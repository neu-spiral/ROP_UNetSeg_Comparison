# A Severity Score For Retinopathy of Prematurity

The code in this repository contains extracting retinopahty of prematurity related features with U-Net segmentation, as well as a multi-expert generative model combining both class and pairwise comparison labels. Details can be found in the paper:
> Automated ROP DiagnosticSystem based on Comparisons and U-Net Segmentation. Peng Tian, Jennifer Dy, Deniz Erdoğmuş, Susan Ostmo, J. Peter Campbell,Michael F. Chiang, and Stratis Ioannidis. InPETRA ’21:ACM International Conference on PErvasive Technologies Related to AssistiveEnvironments, June 25 -July 2nd, 2021, Corfu, Greece.

Note that this work is an extension of the following paper:
> A Severity Score For Retinopathy of Prematurity. Peng Tian, Yuan Guo, Jayashree Kalpathy-Cramer, Susan Ostmo, J. Peter Campbell, Michael F. Chiang, Jennifer Dy, Deniz Erdogmus, Stratis Ioannidis. Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery \& Data Mining

### Python Package Requirement
Python version: 2.7.14

|Package|Version|
|---|---|
|numpy|1.15.0|
|scikit-learn|0.19.1|
|cvxopt|1.2.0|
|cvxpy|0.4.5|
|matplotlib (optional)|2.1.0|

### Segmentation and Feature Extraction
Type following line in the 'Anaconda Prompt' or 'Terminal':
```
python FeatureExtraction/code/mainScript.py "FeatureExtraction/example/" "exampleImages.xlsx" "scoresOfExampleImages.xlsx" -featureFileName Features.xlsx
```
This code evaluates  the features for all images which are listed in the `exampleImages.xlsx`  file and located in the `example` folder which should be located in the 'data' folder.
At the end, the features would be saved in :
```
FeatureExtraction/data/example/Features.xlsx
```
Detailed inputs to mainScript are as follows:

| Option | Description |
| ------ | ----------- |
| pathToFolder |  A string denoting the name of the folder (located under 'data' folder) containing all the images need to be processed and xlsx/csv file which has the image information.  |
| imageNamesFile | A string denoting the '.xlsx' or '.csv' filename in the folder. In this spreadsheet, first column is the image name ending with 'bmp','png',etc. Second column is the corresponding segmentation name. If segmentation images are provided, they should be located under 'Segmented' file under the folder where the color images and imageNames file are located. The third and fourth column are the disc center for the image in (column, row) order. Note that imageNames column is required for code to run, the other columns are optional (if not provided, the system will run additional scripts to determine those information) |
| scoreFileName |  A string denoting the score file name , that would contain the image names and its corresponding severity scores. |
| saveDebug (optional) | If 1 (default) the system will save the debug files (features, vessel centerlines). If 0 is provided, debug files will not be saved.|
|featureFileName (optional) | A string denoting the '.xlsx' or '.csv' file name, that would contain the image names and its features.|
|predictPlus (optional) | If 1 (default) the system will create severity score from Plus vs Not Plus classifier. If 0 is provided, the system will create severity score from Normal vs Not Normal classifier (Please look at the refrences for details). |

The exact packages used in segmentation and feature extraction are provided in `FeatureExtraction/environment.yml`

### Multi-expert Model
To run the multi-expert model on ROP dataset. Please use the following command:

```bash
    python Classifier/main.py --segment auto --expert bias --loss LogLog --alpha 0.5 --lam 1.0 
```
The details of input parameters are:

|Parameter|Description|
|---|---|
|--segment|one of {manual, auto}, which corresponds to manually segmented feature and automatically segmented feature, respectively.|
|--expert| one of {global,bias,expert,all}. Global is global model (GM); bias is global model with expert bias (GMEB); expert is the expert model (EM). All runs all three models (GM, GMEB, EM).|
|--loss|loss function, one of {LogLog, LogSVM, LogSVM, SVMSVM}.|
|--alpha|balance parameter, float number in [0,1]. 0 only trains comparison labels and 1 only trains class labels.|
|--lam|regularization parameter, positive float number.|
    
### Citing This Paper
Please cite the following paper if you intend to use this code for your research.
> Automated ROP DiagnosticSystem based on Comparisons and U-Net Segmentation. Peng Tian, Jennifer Dy, Deniz Erdoğmuş, Susan Ostmo, J. Peter Campbell,Michael F. Chiang, and Stratis Ioannidis. InPETRA ’21:ACM International Conference on PErvasive Technologies Related to AssistiveEnvironments, June 25 -July 2nd, 2021, Corfu, Greece.

The details of feature extraction could be found in the following papers:
> Plus Disease in Retinopathy of Prematurity: Convolutional Neural Network Performance Using a Combined Neural Network and Feature Extraction Approach. Veysi M Yildiz, Peng Tian, Ilkay Yildiz, James M Brown, Jayashree Kalpathy-Cramer, Jennifer Dy, Stratis Ioannidis, Deniz Erdogmus, Susan Ostmo, Sang Jin Kim, R. V. Paul Chan, J. Peter Campbell and Michael F. Chiang. In Translational Vision Science & Technology 9, no. 2 (2020): 10-10

> Computer-Based Image Analysis for Plus Disease Diagnosis in Retinopathy of Prematurity: Performance of the “i-ROP” System and Image Features Associated With Expert Diagnosis. Esra Ataer-Cansizoglu, Veronica Bolon-Canedo, J. Peter Campbell, Alican Bozkurt, Deniz Erdogmus, Jayashree Kalpathy-Cramer, Samir Patel, Karyn Jonas, R. V. Paul Chan, Susan Ostmo, Michael F. Chiang; on behalf of the i-ROP Research Consortium. In Translational Vision Science & Technology 4.6 (2015): 5-5.


### Acknowledgements
Our work is supported by NIH (R01EY019474, P30EY10572), NSF (SCH-1622542 at MGH; SCH-1622536 at Northeastern; SCH-1622679 at OHSU), a Facebook Research Award and by unrestricted departmental funding from Research to Prevent Blindness (OHSU).
