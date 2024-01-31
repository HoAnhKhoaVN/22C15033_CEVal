source D:/Master/OCR_Nom/fulllow_ocr_temple/.venv/Scripts/activate

#####################
## HYPER-PARAMETER ##
#####################
GT_ZIP='gt.zip'


echo "#########################################"
echo "## CONVERT PPOCRLABEL FORMAT TO CLEVAL ##"
echo "#########################################"
GT_LABEL_TXT='D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/final_data/data_demo/demo/go/de/Label.txt'
GT_IMG_PATH='D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/final_data/data_demo/demo/go/de'
GT_PATH='go/de_gt'

python get_gt.py --img_path $GT_IMG_PATH \
                 --label_txt $GT_LABEL_TXT \
                 --gt_path $GT_PATH


echo "##########################################"
echo "## CONVERT PRED PPOCR FORMAT TO CLEVAL  ##"
echo "##########################################"
PRED_JSON_PATH='go/de_pred/pred.json'
PRED_IMG_PATH='D:/Master/OCR_Nom/fulllow_ocr_temple/dataset/final_data/data_demo/demo/go/de'
PRED_PATH='go/de_pred'

mkdir -p $PRED_PATH

python get_pred.py --img_path $PRED_IMG_PATH \
                   --json_path $PRED_JSON_PATH \
                   --pred_path $PRED_PATH
