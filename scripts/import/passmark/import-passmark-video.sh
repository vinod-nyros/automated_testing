import_passmark() {
    python tablescrape_passmark.py $url 3 \
    | python parse_passmark_video.py "$choicecat" "$url" \
    > $choicecat.csv
}

url=http://www.videocardbenchmark.net/high_end_gpus.html
choicecat="High-end GPUs"

import_passmark


