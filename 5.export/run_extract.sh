#!/bin/bash

rm -rf exported

python3 md_extractor.py -d ../1.frontend -e all --exclude-dirs node_modules build --exclude-files package-lock.json -o exported
python3 md_extractor.py -d ../2.backend -e all --exclude-dirs node_modules build uploads --exclude-files package-lock.json -o exported
python3 md_extractor.py -d ../3.local-test -e all --exclude-dirs node_modules build uploads --exclude-files package-lock.json -o exported
python3 md_extractor.py -d ../4.tf-infras -e tf tfvars -o exported

cd ../..
tree -L 2 moviestream > moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt 
tree -L 3 moviestream/1.frontend/src  >> moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt
tree -L 3 moviestream/2.backend/src  >> moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt
tree -L 3 moviestream/3.local-test  >> moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt
tree -L 3 moviestream/4.tf-infras >> moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt

cat moviestream/5.export/exported/extract* >> moviestream/5.export/exported/source_code_$(date '+%Y%m%d_%H%M%S').txt

rm -rf moviestream/5.export/exported/extract*