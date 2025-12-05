library(bookdown)
pdf_book(toc = TRUE,
         number_sections = TRUE,
         fig_caption = TRUE,
         pandoc_args = NULL,
         base_format = rmarkdown::pdf_document,
         toc_unnumbered = TRUE,
         toc_appendix = FALSE,
         toc_bib = FALSE,
         quote_footer = NULL,
         highlight_bw = FALSE)
