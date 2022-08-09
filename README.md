# rpfbagr

[![Github Version](https://img.shields.io/github/v/release/brsynth/rpfbagr?display_name=tag&sort=semver)](version) [![Conda Version](https://img.shields.io/conda/vn/bioconda/rpfbagr.svg)](https://anaconda.org/bioconda/rpfbagr)  
[![GitHub Super-Linter](https://github.com/brsynth/rpfbagr/workflows/Tests/badge.svg)](https://github.com/marketplace/actions/super-linter) [![Coverage](https://img.shields.io/coveralls/github/brsynth/rpfbagr)](coveralls)  
[![License](https://img.shields.io/github/license/brsynth/rpfbagr)](license) [![DOI](https://zenodo.org/badge/436924636.svg)](https://zenodo.org/badge/latestdoi/436924636) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![Gitter](https://badges.gitter.im/BioRetroSynth/SynBioCAD.svg)](https://gitter.im/BioRetroSynth/SynBioCAD?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)  

## Description

*rpfbagr* provides a cli interface to predict gene knockout targets with an heterologous pathway  

## Installation

### Conda

```sh
conda install -c bioconda rpfbagr
```

### Docker

```sh
docker pull ghcr.io/brsynth/rpfbagr:<release version>
```

### Pip

Download asset from the last *Releases*.  

* Unzip asset  

```sh
unzip <folder>
```  

* Install *wheel* with *pip*  

```sh
pip install <unzipped file>.whl
```  

## Usage

Example: Define the best combination of genes deletion to optimize a target.

```sh
python -m rpfbagr \
    [input files]
    --input-model-file <SBML file>
    --input-pathway-file <SBML file>
    --input-medium-file <CSV file>
    [input parameters]
    --biomass-rxn-id <id reaction, str>
    --target-rxn-id <id reaction, str>
    --substrate-rxn-id <id reaction, str>
    [output file]
    --output-file <CSV file>
```

Or with docker:  

```sh
docker run \
    -it \
    --rm \
    -v $PWD:/data \
    rpfbagr:latest \
    --input-model /data/<SBML file> \
    --input-pathway-file /data/<SBML file> \
    --input-medium-file /data/<CSV file> \
    --biomass-rxn-id <id reaction, str> \
    --target-rxn-id <id reaction, str> \
    --substrate-rxn-id <id reaction, str>
    --output-file /data/<CSV file>
```

## Tests

*pytest* is installed with this package.

```sh
cd <repository>
python -m pytest
```

## Built with these main libraries

* [cameo](https://github.com/biosustain/cameo) - Computer aided metabolic engineering & optimization
* [cobrapy](https://github.com/opencobra/cobrapy) - Constraint-based modeling of metabolic networks
* [Pandas](https://github.com/pandas-dev/pandas) - Essential dataframe object

## Authors

* **Guillaume Gricourt**

## Licence

See the LICENCE file for details.
