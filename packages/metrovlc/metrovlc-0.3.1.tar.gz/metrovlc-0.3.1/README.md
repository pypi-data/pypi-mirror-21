# METROVLC

[![pypi-version][badge-pypi-version]][pypi]
[![Open issues][badge-issues]][issues]
[![License][badge-license]][license]

Utilidad en línea de comandos para [MetroValencia].

## Descripción

Recupera alguna de las funcionalidades de la web de MetroValencia desde
tu terminal.

## Requerimientos

 * Python3

## Instalación

```shell
pip install metrovlc
```

## Ayuda
### Uso

```
# metrovlc --help
usage: metrovlc [-h] [-b BONO] [-d ORIGEN DESTINO] [-ss] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -b BONO, --bono BONO  Bono info
  -d ORIGEN DESTINO, --horario ORIGEN DESTINO
                        Horarios para ORIGEN -> DESTINO
  -ss, --solo-saldo     Solo muestra el saldo disponible
  -v, --version         show program's version number and exit
```

### Ejemplos
```shell
# Mirar saldo de tu tarjeta TuiN
$ metrovlc -b 4065483771
Bono: 4065483771, Título: TuiN, saldo: 5,67 Euros

# Mirar saldo de tu tarjeta TuiN, solo saldo
$ metrovlc -b 4065483771 -ss
5,67

# Horarios de Llíria a Campanar
$ metrovlc -horarios lliria campanar

Estación de Origen: Llíria
Estación de Destino: Campanar
Franja horaria: de 00:00 a 23:59
Día: 16/03/2017
Duración aproximada del trayecto: 48 minutos aprox.
Para efectuar este trayecto es necesario un billete de las zonas: ABC
De Llíria a Campanar, Trenes con destino: València Sud, Torrent Avinguda, Hora de salida

02 | 02:38 | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
06 | 06:09 | 06:37 | 06:52 | ----- | ----- | ----- | ----- | ----- |
07 | 07:07 | 07:22 | 07:37 | 07:52 | ----- | ----- | ----- | ----- |
08 | 08:07 | 08:22 | 08:39 | ----- | ----- | ----- | ----- | ----- |
09 | 09:09 | 09:39 | ----- | ----- | ----- | ----- | ----- | ----- |
10 | 10:09 | 10:39 | ----- | ----- | ----- | ----- | ----- | ----- |
11 | 11:09 | 11:39 | ----- | ----- | ----- | ----- | ----- | ----- |
12 | 12:09 | 12:39 | ----- | ----- | ----- | ----- | ----- | ----- |
13 | 13:09 | 13:39 | ----- | ----- | ----- | ----- | ----- | ----- |
14 | 14:09 | 14:37 | 14:52 | ----- | ----- | ----- | ----- | ----- |
15 | 15:07 | 15:22 | 15:39 | ----- | ----- | ----- | ----- | ----- |
16 | 16:09 | 16:39 | ----- | ----- | ----- | ----- | ----- | ----- |
17 | 17:09 | 17:39 | ----- | ----- | ----- | ----- | ----- | ----- |
18 | 18:09 | 18:39 | ----- | ----- | ----- | ----- | ----- | ----- |
19 | 19:09 | 19:39 | ----- | ----- | ----- | ----- | ----- | ----- |
20 | 20:09 | 20:39 | ----- | ----- | ----- | ----- | ----- | ----- |
21 | 21:09 | 21:39 | ----- | ----- | ----- | ----- | ----- | ----- |
22 | 22:09 | 22:41 | ----- | ----- | ----- | ----- | ----- | ----- |
23 | 23:14 | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
```

## Licencia

MIT

[MetroValencia]:http://www.metrovalencia.es/page.php?idioma=_es
[bad-travis]:https://api.travis-ci.org/penicolas/metrovlc.svg?branch=master
[badge-travis]:https://img.shields.io/travis/penicolas/metrovlc.svg?style=flat-square
[badge-coveralls]:https://img.shields.io/coveralls/penicolas/metrovlc.svg?style=flat-square
[badge-issues]:http://img.shields.io/github/issues/penicolas/metrovlc.svg?style=flat-square
[badge-license]:http://img.shields.io/badge/license-MIT-blue.svg?style=flat-square
[badge-pypi-version]:https://img.shields.io/pypi/v/metrovlc.svg?style=flat-square
[travis]:https://travis-ci.org/penicolas/metrovlc
[coveralls]:https://coveralls.io/github/penicolas/metrovlc
[heuristics]:https://github.com/penicolas/metrovlc/issues/2
[issues]:https://github.com/penicolas/metrovlc/issues
[pypi]:https://pypi.python.org/pypi?:action=display&name=metrovlc
[license]:LICENSE
