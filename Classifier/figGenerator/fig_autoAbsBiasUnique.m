% This script is to draw the pdf figure that compare the all experts model,
% expert bias model and every experts model.
% Input :
%       - fileLoad: string that specify the mat file that generated by
%       dataOrganizer.m
%       - figSave: string that figure file saved and must end with '.pdf'
close all;
fileLoadPath = '../../data/ropResult/auto_SVMSVM.mat';
fileRSDPath = '../../data/ropResult/auto_RSD_SVMSVM.mat';
figSave = '../../pic/SVMSVM';
isSaveFig = 1;

xAxis = 0:0.1:1;
classPred = 'Automatically';
legendStr = {'GM', 'GMEB', 'EM'};
xLabel = 'Weight \alpha on Class Label Data';
titlePlus = ['Plus vs Not Plus of ' classPred ' Segmented Features'];
titlePreP = ['Not Normal vs Normal of ' classPred ' Segmentation Features'];


file = load(fileLoadPath);
fileRSD = load(fileRSDPath);
% Figure 1  Plus vs Not Plus for the diagnostic labels.
auc4AbsPlus = [file.bestAbs2AbsPlusAUC(:,1),file.bestBias2AbsPlusAUC(:,1),file.bestUnique2AbsPlusAUC(:,1)];
aucCI4AbsPlus = 1.96*[file.bestAbs2AbsPlusAUC(:,2),file.bestBias2AbsPlusAUC(:,2),file.bestUnique2AbsPlusAUC(:,2)];
fig1 = plotAUCCI(auc4AbsPlus,aucCI4AbsPlus,'xLabel',xLabel,...
    'yLabel','AUC on Class Labels','legendStr',legendStr,'isSaveFig',isSaveFig,...
    'figName',[figSave,'_Abs_Plus_',classPred],'xAxis',xAxis);


% Figure 2  Plus vs Not Plus for Comparison labels.
auc4CmpPlus = [file.bestAbs2CmpPlusAUC(:,1),file.bestBias2CmpPlusAUC(:,1),file.bestUnique2CmpPlusAUC(:,1)];
aucCI4CmpPlus = 1.96*[file.bestAbs2CmpPlusAUC(:,2),file.bestBias2CmpPlusAUC(:,2),file.bestUnique2CmpPlusAUC(:,2)];
fig3 = plotAUCCI(auc4CmpPlus,aucCI4CmpPlus,'xLabel',xLabel,...
    'yLabel','AUC on Comparison Labels','legendStr',legendStr,'isSaveFig',isSaveFig,...
    'figName',[figSave,'_Cmp_Plus_',classPred],'xAxis',xAxis);

% Figure 3  Plus vs Not Plus for the concensus RSD labels.
auc4RSDPlus = [fileRSD.bestRSD2RSDPlusAUC(:,1),file.bestBias2RSDPlusAUC(:,1)];
aucCI4RSDPlus = 1.96*[fileRSD.bestRSD2RSDPlusAUC(:,2),file.bestBias2RSDPlusAUC(:,2)];
fig5 = plotAUCCI(auc4RSDPlus,aucCI4RSDPlus,'xLabel',xLabel,...
    'yLabel','AUC on RSD Labels','legendStr',{'Training RSD Labels','GMEB'},'isSaveFig',isSaveFig,...
    'figName',[figSave,'_RSD_Plus_',classPred],'xAxis',xAxis);    
    