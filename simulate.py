from q1 import create_processes, FIFO, aging
import matplotlib.pyplot as plt
import csv
import os
from statistics import mean
from datetime import datetime

# Configurações da simulação
NUM_EXECUCOES = 10
FRAME_RANGE = list(range(5, 51, 5))

def simular():
    resultados = []

    for exec_num in range(NUM_EXECUCOES):
        print(f"Execução {exec_num + 1}/{NUM_EXECUCOES}")
        processes = create_processes()
        total_refs = sum(len(p.references) for p in processes)

        for frames in FRAME_RANGE:
            fifo_faults = FIFO(processes, frames)
            aging_faults = aging(processes, frames)

            fifo_rate = fifo_faults * 1000 / total_refs
            aging_rate = aging_faults * 1000 / total_refs

            resultados.append({
                "execucao": exec_num + 1,
                "molduras": frames,
                "fifo": fifo_rate,
                "aging": aging_rate
            })

    return resultados

def calcular_medias(resultados):
    medias = []

    for frames in FRAME_RANGE:
        fifo_vals = [r["fifo"] for r in resultados if r["molduras"] == frames]
        aging_vals = [r["aging"] for r in resultados if r["molduras"] == frames]

        medias.append({
            "molduras": frames,
            "fifo_medio": mean(fifo_vals),
            "aging_medio": mean(aging_vals)
        })

    return medias

def salvar_csv(medias, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Molduras", "FIFO (médio)", "Aging (médio)"])
        for row in medias:
            writer.writerow([row["molduras"], f"{row['fifo_medio']:.2f}", f"{row['aging_medio']:.2f}"])

def plotar_grafico(medias, img_filename):
    frames = [m["molduras"] for m in medias]
    fifo = [m["fifo_medio"] for m in medias]
    aging = [m["aging_medio"] for m in medias]

    plt.figure(figsize=(10, 6))
    plt.plot(frames, fifo, marker='o', label="FIFO (médio)")
    plt.plot(frames, aging, marker='s', label="Aging (médio)")
    plt.xlabel("Número de Molduras de Página")
    plt.ylabel("Faltas de Página por 1000 Referências")
    plt.title("Comparação FIFO vs Aging (médias de múltiplas execuções)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(img_filename)
    plt.show()

def main():
    resultados = simular()
    medias = calcular_medias(resultados)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = "resultados"
    os.makedirs(output_folder, exist_ok=True)

    csv_filename = os.path.join(output_folder, f"medias_{timestamp}.csv")
    img_filename = os.path.join(output_folder, f"grafico_{timestamp}.png")

    salvar_csv(medias, csv_filename)
    plotar_grafico(medias, img_filename)

    print(f"\nResultados salvos em:\n→ CSV: {csv_filename}\n→ Imagem: {img_filename}")

if __name__ == "__main__":
    main()
