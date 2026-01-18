import matplotlib.pyplot as plt
import seaborn as sns

def gerar_heatmap(df):
    plt.figure(figsize=(8, 5))
    sns.heatmap(
        df.pivot_table(
            index='hora',
            columns='tipo_voo',
            values='score_risco_ultima',
            aggfunc='mean'
        ),
        cmap='Reds',
        annot=True
    )

    plt.title("Heatmap Horário – Risco SLA (Última Bagagem)")
    plt.tight_layout()
    plt.savefig("saidas/graficos/heatmap_risco_horario.png")
    plt.show()
