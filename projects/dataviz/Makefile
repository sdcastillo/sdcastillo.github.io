all:index.html

DATA_FILES = $(wildcard data/*.R)
DATA_RDA = $(DATA_FILES:R=rda)

data/%.rda:data/%.R
	Rscript -e "source('$<')"

index.html:index.Rmd css/custom.css $(DATA_RDA) theme_soa.R
	Rscript -e "rmarkdown::render('$<')"

clean:
	rm -rf data/*.rda
	rm index.html
