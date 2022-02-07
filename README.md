Projeto QGIS Monitor de Secas
-----------------------

Em apoio à operacionalização do Monitor de Secas, objetiva-se automatizar a criação do projeto QGIS e das figuras de apoio para o traçado do mapa de seca pelos autores, tornando o processo mais ágil, simples e consistente.

Instalação
----------------------

* Certifique-se que o QGIS 2.14 ou 2.18 esteja instalado (não testado com outras versões).
* Faça o git clone para o seu computador.
* Altere o diretório para a pasta dos scripts através do comando `cd ...`:
    * Ex.: `cd /home/funceme/monitor/scripts`
* Instale os módulos requeridos:
    * Certifique-se que está usando Python 2.
    * Um ambiente virtual pode ser criado para esta operação.
    * Executar `cat packages.txt | xargs sudo apt-get install`
    * Executar `pip install -r requirements.txt`
    * Executar `pip install GDAL==$(gdal-config --version)`

Operação
-----------------------

Verifique o `manual.pdf` para exemplos de uso das rotinas.

Extendendo este projeto
-------------------------

Se deseja extender este trabalho, aqui encontram-se algumas etapas ainda manuais que podem ser automatizadas:

* Incluir o indicador ESI no processo.
* Importação do arquivo `.qpt` (template) no projeto QGIS pela rotina `project_gen.py`.
* Download dos shapes do traçado mais recente nas pastas e organiza-los no projeto QGIS pela rotina `project_gen.py`.
* Remoção de figuras desnecessárias geradas da pasta FIGS_APOIO.
* Organização das pastas de forma similar ao OwnCloud.
* Compressao dos dados finais em formato `.zip`.
