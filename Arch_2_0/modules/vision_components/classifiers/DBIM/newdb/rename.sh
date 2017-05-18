for f in *.jpg; do
    mv "$f" "${f/.jpg/_1.jpg}"
done