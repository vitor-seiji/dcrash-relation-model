def geocodificar_dataframe(df):
    """Geocodifica DataFrame completo"""
    print("="*70)
    print("GEOCODIFICAÇÃO OFFLINE DE ALTA PRECISÃO")
    print("="*70)
    print(f"Rodovias mapeadas: {len(INTERPOLADORES)}")
    print(f"Registros: {len(df)}\n")
    
    if 'latitude' not in df.columns:
        df['latitude'] = np.nan
    if 'longitude' not in df.columns:
        df['longitude'] = np.nan
    if 'metodo_geocoding' not in df.columns:
        df['metodo_geocoding'] = ''
    
    for idx, row in df.iterrows():
        if pd.notna(row.get('latitude')) and pd.notna(row.get('longitude')):
            continue
        
        lat, lon, metodo = geocodificar_linha(row['rodovia'], row['km'])
        df.at[idx, 'latitude'] = lat
        df.at[idx, 'longitude'] = lon
        df.at[idx, 'metodo_geocoding'] = metodo
    
    print("\n" + "="*70)
    print("RELATÓRIO")
    print("="*70)
    stats = df['metodo_geocoding'].value_counts()
    print(stats)
    
    sucesso = len(df[df['metodo_geocoding'].isin(['interpolado', 'antes_inicio', 'apos_fim'])])
    taxa = (sucesso / len(df) * 100) if len(df) > 0 else 0
    print(f"\nSucesso: {taxa:.1f}% ({sucesso}/{len(df)})")
    
    # Mostrar rodovias não encontradas
    nao_encontradas = df[df['metodo_geocoding'] == 'nao_encontrado']
    if len(nao_encontradas) > 0:
        rodovias_unicas = nao_encontradas['rodovia'].apply(normalizar_rodovia).unique()
        print(f"\n⚠️  {len(rodovias_unicas)} rodovias não mapeadas:")
        for rod in sorted(rodovias_unicas):
            count = len(nao_encontradas[nao_encontradas['rodovia'].apply(normalizar_rodovia) == rod])
            print(f"  - {rod} ({count} registros)")
    else:
        print("\n✅ Todas as rodovias foram geocodificadas!")
    
    return df