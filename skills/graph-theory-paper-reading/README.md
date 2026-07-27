# graph-theory-paper-reading

A coding-agent skill for deep reading of graph theory papers. Generates structured LaTeX reports with color-coded proof trees as standalone vector images.

## Features

- **6-dimension deep reading**: Research topic identification, core definition extraction, literature review, main theorem improvement analysis, proof outline + proof tree construction, future research directions.
- **Proof tree visualization**: Color-coded forest/TikZ trees rendered as standalone PDF vector images.
- **PDF auto-conversion**: Uses MinerU to convert PDF papers to Markdown when direct PDF reading is unavailable.
- **LaTeX output**: Generates `xelatex`-compilable `.tex` files for main report and each proof tree.

## Dependencies

| Layer | Requirement | Package |
|-------|------------|---------|
| PDF conversion | Optional MinerU CLI | Install only after explicit user approval |
| LaTeX compilation | XeLaTeX + packages | `ctex`, `forest`, `standalone`, `amsmath`, `amssymb`, `graphicx`, `titlesec`, `xcolor`, `framed`, `longtable`, `booktabs`, `enumitem`, `hyperref` |
| Fonts | CJK fonts for Chinese | Included in TeX Live (macOS: STSong) |

## Quick Test

```bash
# 1. Verify optional MinerU
pip3 show mineru && echo "OK" || echo "Optional dependency is not installed"

# 2. Verify XeLaTeX + forest
xelatex --version && echo "OK" || echo "Install TeX Live"
kpsewhich forest.sty && echo "OK" || echo "Install: tlmgr install forest"

# 3. Compile a minimal proof tree
cat > /tmp/test_tree.tex << 'EOF'
\documentclass[tikz,border=5pt]{standalone}
\usepackage{forest}
\begin{document}
\begin{forest}
  for tree={grow'=south, draw, align=left},
  [Root [Child A] [Child B]]
\end{forest}
\end{document}
EOF
xelatex -interaction=nonstopmode -output-directory=/tmp /tmp/test_tree.tex && echo "Tree OK" || echo "FAIL"
```

## License

MIT — See individual papers' copyright for generated reports.

## Contributor

Course contributor: **Zhuojie Tu**. See
[`PROVENANCE.yaml`](PROVENANCE.yaml) and
[`NORMALIZATION.md`](NORMALIZATION.md) for the course-edition record.
