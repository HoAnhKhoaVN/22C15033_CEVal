source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

echo "############"
echo "## CLEVAL ##"
echo "############"

GT_PATH='ground_truth.zip'
PRED_PATH='prediction.zip'
PROFILE='profile_go_de.txt'


cleval -g=$GT_PATH \
       -s=$PRED_PATH \
       --E2E \
       -v \
       --DEBUG \
       --PROFILE > $PROFILE