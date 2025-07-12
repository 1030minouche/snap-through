import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import imageio.v2 as imageio
from pathlib import Path
import argparse
import io
from tqdm import tqdm

def detect_band_position(image_path):
    img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Erreur de chargement : {image_path}")
    center_x = img.shape[1] // 2
    column = img[:, center_x]
    min_index = np.argmin(column)
    return min_index

def get_images(directory, ext=".tiff"):
    files = sorted(Path(directory).glob(f"*{ext}"), key=lambda x: int(x.stem.split("_")[-1]))
    if not files:
        raise FileNotFoundError(f"Aucune image .tiff dans {directory}")
    return files

def annotate_image_with_graph(image_path, band_y, all_positions, times, index, output_dir):
    img = cv2.imread(str(image_path))
    height, width = img.shape[:2]

    if band_y is not None:
        cv2.line(img, (0, int(band_y)), (width, int(band_y)), (0, 0, 255), 2)

    fig, ax = plt.subplots(figsize=(4, height / 100))
    ax.plot(times, all_positions, label="Position Y")
    ax.axvline(times[index], color='red', linestyle='--', label='Image actuelle')
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Position (px)")
    ax.set_title(f"t = {times[index]:.2f} s")
    ax.invert_yaxis()
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    graph_img = cv2.imdecode(np.frombuffer(buf.read(), np.uint8), cv2.IMREAD_COLOR)

    if graph_img.shape[0] != height:
        scale = height / graph_img.shape[0]
        new_width = int(graph_img.shape[1] * scale)
        graph_img = cv2.resize(graph_img, (new_width, height))

    combined = np.hstack((img, graph_img))
    out_path = Path(output_dir) / f"frame_{index:04}.png"
    cv2.imwrite(str(out_path), combined)
    return out_path

def save_global_graph(positions, times, output_dir):
    plt.figure(figsize=(8, 4))
    plt.plot(times, positions, marker='x', linestyle='-')
    plt.title("Évolution verticale de la bandelette")
    plt.xlabel("Temps (s)")
    plt.ylabel("Position (px)")
    plt.gca().invert_yaxis()
    plt.grid()
    plt.tight_layout()
    plt.savefig(Path(output_dir) / "graph_position.jpg")
    plt.close()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='images', help='Dossier des images')
    parser.add_argument('--output', default='sortie', help='Dossier de sortie')
    parser.add_argument('--fps', type=float, default=5.0, help='Images par seconde (FPS)')
    return parser.parse_args()

def main():
    args = parse_args()
    input_dir = args.input
    output_dir = args.output
    fps = args.fps
    Path(output_dir).mkdir(exist_ok=True)

    images = get_images(input_dir)
    positions = []
    times = [i / fps for i in range(len(images))]

    print("Analyse des images...")
    for path in tqdm(images, desc="Détection"):
        pos = detect_band_position(path)
        positions.append(pos)

    df = pd.DataFrame({
        "image": [p.name for p in images],
        "temps_s": times,
        "position_y": positions
    })
    df.to_csv(Path(output_dir) / "positions_bandelette.csv", index=False)

    save_global_graph(positions, times, output_dir)

    print("Création des images annotées...")
    annotated_paths = []
    for i, path in enumerate(tqdm(images, desc="Annotation")):
        annotated_path = annotate_image_with_graph(path, positions[i], positions, times, i, output_dir)
        annotated_paths.append(annotated_path)

    print("Création du GIF...")
    gif_frames = [imageio.imread(p) for p in annotated_paths]
    imageio.mimsave(Path(output_dir) / "bandelette.gif", gif_frames, duration=1.0 / fps)

    print("Création de la vidéo MP4...")
    h, w, _ = cv2.imread(str(annotated_paths[0])).shape
    video_path = str(Path(output_dir) / "bandelette.mp4")
    video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))
    for p in annotated_paths:
        video.write(cv2.imread(str(p)))
    video.release()

    print("Terminé. Résultats dans :", output_dir)

if __name__ == "__main__":
    main()
