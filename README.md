# Scraping-plataformas de trabajo
Obtener la información de los aplicantes a un determinado puesto de trabajo

## Comandos

### Actualizar archivos de configuracion
```bash
python update_json.py --company_name japisale --config_file bumeran.json --process_name "asistente de marketing" --job_page "url de prueba2"

```

### Ejecucion de programa
```bash
python scraping_bumeran.py --company_name japisale --config_file bumeran.json --process_name "asistente de marketing"
```
- `--company_name`: nombre de la compania
- `--confi_file`: nombre del archivo de configuracion a usar en funcion de la compania
- `--process_name`: nombre del puesto de trabajo al que se va a hacer scraping y que debe estar en el archivo de configuracion.
