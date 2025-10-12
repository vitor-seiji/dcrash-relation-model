def normalizar_rodovia(nome):
    """Normaliza nome da rodovia"""
    nome = str(nome).strip().upper()
    nome = nome.rstrip('EDNSLO')
    
    if '/' in nome:
        partes = nome.split('/')
        nome = partes[1] if len(partes) > 1 else partes[0]
    
    for prefix in ['SPA', 'SPI', 'SPD', 'SPM']:
        if nome.startswith(prefix):
            nome = nome[len(prefix):]
            break
    
    if nome.startswith('AVM'):
        return 'SP-021'
    
    if not nome.startswith('SP-'):
        if nome.startswith('SP'):
            nome = 'SP-' + nome[2:]
        else:
            nome = 'SP-' + nome
    
    return nome

def criar_interpolador_cubico(pontos):
    """Cria interpolador spline cúbico de alta qualidade"""
    kms = np.array([p[0] for p in pontos])
    lats = np.array([p[1] for p in pontos])
    lons = np.array([p[2] for p in pontos])
    
    # Usar CubicSpline que garante continuidade suave
    cs_lat = CubicSpline(kms, lats, bc_type='natural')
    cs_lon = CubicSpline(kms, lons, bc_type='natural')
    
    return cs_lat, cs_lon, kms.min(), kms.max()

# Pré-computar todos os interpoladores
INTERPOLADORES = {}
for rod, pontos in RODOVIAS_DETALHADAS.items():
    INTERPOLADORES[rod] = criar_interpolador_cubico(pontos)

print(f"Sistema iniciado com {len(INTERPOLADORES)} rodovias mapeadas")

def geocodificar_linha(rodovia, km):
    """Geocodifica uma linha com alta precisão"""
    rodovia_norm = normalizar_rodovia(rodovia)
    
    if rodovia_norm not in INTERPOLADORES:
        return None, None, 'nao_encontrado'
    
    try:
        km_num = float(km)
    except:
        return None, None, 'erro_km'
    
    cs_lat, cs_lon, km_min, km_max = INTERPOLADORES[rodovia_norm]
    
    # Limitar extrapolação
    km_interp = np.clip(km_num, km_min * 0.95, km_max * 1.05)
    
    # Interpolar
    lat = float(cs_lat(km_interp))
    lon = float(cs_lon(km_interp))
    
    # Validar resultados
    if not (-25.5 < lat < -19.5 and -54.0 < lon < -44.0):
        return None, None, 'fora_sp'
    
    # Determinar método
    if km_num < km_min:
        metodo = 'antes_inicio'
    elif km_num > km_max:
        metodo = 'apos_fim'
    else:
        metodo = 'interpolado'
    
    return round(lat, 6), round(lon, 6), metodo