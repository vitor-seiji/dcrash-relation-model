df = pd.read_csv("Acidentes.csv", dtype={8: str, 11: str})
print(f"Dataset: {df.shape[0]:,} linhas")

# Variáveis temporais
df["data"] = pd.to_datetime(df["data"], errors="coerce")
df["ano"] = df["data"].dt.year
df["mes"] = df["data"].dt.month
df["dia_semana"] = df["data"].dt.weekday
df["hora"] = df["data"].dt.hour
df["fim_semana"] = (df["dia_semana"] >= 5).astype(int)

# Fatores agravantes
df['fatores_agravantes'] = (
    df['hora'].isin([0,1,2,3,4,5,22,23]).astype(int) +  # Madrugada/noite
    df['fim_semana'] +  # Fim de semana
    df['mes'].isin([12, 1, 6, 7]).astype(int)  # Meses críticos
)

# Classificação de severidade
df['severidade'] = 0  # LEVE
grave_mask = ((df['fatalidades'] >= 2) | ((df['fatalidades'] == 1) & (df['fatores_agravantes'] >= 2)))
medio_mask = (((df['fatalidades'] == 1) & (df['fatores_agravantes'] < 2)) | ((df['fatalidades'] == 0) & (df['fatores_agravantes'] >= 3)))
df.loc[grave_mask, 'severidade'] = 2  # GRAVE
df.loc[medio_mask & (df['severidade'] == 0), 'severidade'] = 1  # MÉDIO

labels = ['LEVE', 'MÉDIO', 'GRAVE']
print(f"Classes: {[f'{labels[i]}: {c:,} ({c/len(df)*100:.1f}%)' for i, c in enumerate(df['severidade'].value_counts().sort_index())]}")
