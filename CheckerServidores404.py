# -*- coding: utf-8 -*-
# ================================
#   SERVER STATUS SCANNER
#   Compatible con QPython 3
# ================================

import os
import requests
import threading
from urllib.parse import urlparse
from datetime import datetime

# ================================
# BANNER ASCII
# ================================
def banner():
    cadena_tiempo_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color_dinamico = "\033[38;5;208m"
    
    print(f"\n\n\n\033[0m\033[38;5;135m{cadena_tiempo_inicio}\033[0m")
    print(f"\033[38;5;123m{'═' * 42}\033[0m")
    print(f"\033[1;38;5;221m        🌎 SERVIDORES ONLINE 🌎   \033[0m")
    print(f"{color_dinamico}        🎸 Creador ERROR404 🎸   \033[0m")
    print(f"\033[38;5;197m          ⚡ Version 1.0 ⚡\033[0m")
    print(f"\033[38;5;123m{'═' * 42}\033[0m\n")


# ================================
# CONFIGURACIÓN DE CARPETAS
# ================================
COMBO_PATH = "/sdcard/combo/"
HITS_PATH = "/sdcard/hits/"

if not os.path.exists(HITS_PATH):
    os.makedirs(HITS_PATH)


# ================================
# LISTAR ARCHIVOS TXT
# ================================
def listar_archivos():
    archivos = [f for f in os.listdir(COMBO_PATH) if f.endswith(".txt")]
    if not archivos:
        print("No hay archivos .txt en la carpeta combo")
        return None
    
    print("Archivos disponibles:\n")
    for i, archivo in enumerate(archivos):
        print(f"[{i}] {archivo}")
    
    opcion = int(input("\nElige el número del archivo: "))
    return os.path.join(COMBO_PATH, archivos[opcion])


# ================================
# EXTRAER HOST
# ================================
def extraer_host(linea):
    linea = linea.strip()
    
    if linea.startswith("http"):
        return linea
    
    if ":" in linea:
        partes = linea.split(":")
        if len(partes) >= 2:
            return "http://" + partes[0] + ":" + partes[1]
    
    return None


# ================================
# VERIFICAR SERVIDOR
# ================================
def check_server(url, proxies=None):
    try:
        r = requests.get(url, timeout=5, proxies=proxies)
        if r.status_code < 400:
            print(f"🟢 [ONLINE] {url}")
            with open(HITS_PATH + "online.txt", "a") as f:
                f.write(url + "\n")
        else:
            print(f"🔴 [OFFLINE] {url}")
    except:
        print(f"🔴 [OFFLINE] {url}")


# ================================
# PROXIES
# ================================
def cargar_proxies():
    usar = input("¿Usar proxies? (s/n): ").lower()
    if usar == "s":
        proxy_file = input("Ruta del archivo proxy (.txt): ")
        if os.path.exists(proxy_file):
            with open(proxy_file, "r") as f:
                proxy_list = [line.strip() for line in f if line.strip()]
            return proxy_list
    return None


# ================================
# MAIN
# ================================
def main():
    banner()
    
    archivo = listar_archivos()
    if not archivo:
        return
    
    proxies_list = cargar_proxies()
    
    with open(archivo, "r") as f:
        lineas = f.readlines()
    
    threads = []
    
    for linea in lineas:
        url = extraer_host(linea)
        if url:
            proxy_dict = None
            if proxies_list:
                proxy = proxies_list[len(threads) % len(proxies_list)]
                proxy_dict = {
                    "http": "http://" + proxy,
                    "https": "http://" + proxy
                }
            
            t = threading.Thread(target=check_server, args=(url, proxy_dict))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()
    
    print("\nEscaneo finalizado.")
    print("Resultados guardados en /sdcard/hits/online.txt")


if __name__ == "__main__":
    main()
