source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

#####################
## HYPER-PARAMETER ##
#####################
ROOT='D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/final_data/data_demo/demo/go/de'
GT_PATH='go/de/de_gt'
PRED_PATH='go/de/de_pred_preprocess'
PRED_JSON_PATH='go/de/de_pred_preprocess/pred.json'
PROFILE='go/de/de_pred_preprocess.txt'

#####################
## HYPER-PARAMETER ##
#####################

mkdir -p $PRED_PATH
mkdir -p $GT_PATH

GT_LABEL_TXT=$ROOT'/Label.txt'
GT_ZIP='gt.zip'
PRED_ZIP='pred.zip'

echo ""
echo "############################################"
echo "## 1. CONVERT PPOCRLABEL FORMAT TO CLEVAL ##"
echo "############################################"
echo ""
python get_gt.py --img_path $ROOT \
                 --label_txt $GT_LABEL_TXT \
                 --gt_path $GT_PATH

python zip_file.py --fd_path $GT_PATH \
                   --zip_path $GT_ZIP
echo ""
echo "#############################################"
echo "## 2. CONVERT PRED PPOCR FORMAT TO CLEVAL  ##"
echo "#############################################"
echo ""
python predict/pred_ppocr_with_preprocess.py --img_path $ROOT \
                   --json_path $PRED_JSON_PATH \
                   --pred_path $PRED_PATH

python zip_file.py --fd_path $PRED_PATH \
                   --zip_path $PRED_ZIP

echo ""
echo "###############"
echo "## 3. CLEVAL ##"
echo "###############"
echo ""

cleval -g="$GT_PATH/$GT_ZIP" \
       -s="$PRED_PATH/$PRED_ZIP" \
       --E2E \
       -v > $PROFILE

echo Save to $PROFILE
echo ===== THE END =====