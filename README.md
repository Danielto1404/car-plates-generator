# Car plates GAN

CarPlateGAN – GAN which generates fake square car numbers

## Quick links

* [Example](#example)
* [Installation](#installation)
* [Scrapping tools](#scraping)
* [Related works](#related-works)

## Example:

```python

```

## Installation

```shell
$ pip install git+https://github.com/Danielto1404/car-plates-generation
```

## Scraping

This repository additionally provides scraping tools for [PlatesMania.com](https://platesmania.com/) website.
<br>
### Example of usage:

```python
from car_plate_gan.scraping.plates_mania import PlatesManiaDownloader, Country

downloader = PlatesManiaDownloader(
    root="dataset",      # root path of your dataset
    country=Country.RU   # country
)

downloader.download(from_page=10, to_page=20)
```

## Related works:

* [On realistic generation of new format license plate on vehicle images](https://www.sciencedirect.com/science/article/pii/S1877050921020603)
* [Adversarial Generation of Training Examples: Applications to Moving Vehicle License Plate Recognition](https://arxiv.org/pdf/1707.03124.pdf)
