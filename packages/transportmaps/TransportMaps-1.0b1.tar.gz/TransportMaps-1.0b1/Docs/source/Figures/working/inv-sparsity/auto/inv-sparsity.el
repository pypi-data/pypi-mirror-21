(TeX-add-style-hook
 "inv-sparsity"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("xcolor" "dvipsnames")))
   (TeX-run-style-hooks
    "latex2e"
    "stylesTikzGraphs"
    "tikz_sparsityVolHyper"
    "article"
    "art10"
    "xcolor"
    "caption"
    "subcaption"
    "graphicx"
    "tikz"
    "pgfplots"))
 :latex)

