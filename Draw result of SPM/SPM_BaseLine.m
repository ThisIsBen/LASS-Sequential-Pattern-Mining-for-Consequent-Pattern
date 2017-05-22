

function csv2fft=SPM_BaseLine(accessMeasurement)
close all;


 %disable output file visibility,just save it anyway
figure('Visible','off')


fileDir=strcat('./',accessMeasurement);
fileDir=strcat(fileDir,'/');
files=dir(strcat(fileDir,'*.csv'));
for fileIndex = 1:size(files,1)
        disp(files(fileIndex).name)
        
        fileDir=strcat(fileDir,files(fileIndex).name);
        nonDataRow=3
        drawTheLastPartofData=0.85
        DataLength=csvread(fileDir,nonDataRow,0);
        A = csvread(fileDir,round(length(DataLength)*drawTheLastPartofData)+nonDataRow,0);
       
        RMSE=csvread(fileDir,1,0,[1,0,1,1]);
       
        xid=A(:,1);
        
        actual = A(:,2);
        
        SPM=A(:,3);
        RMSE_SPM=RMSE(1)
        RMSE_BaseLine=RMSE(2)
        
        BaseLine=A(:,4);
        
        
        %set where to draw the "Prediction Start " straight line.
        PredictionLength=12;
       
        
        
        
        
  

    
       
        
        
         fig = figure;
         ax1 = axes('Position',[0 0 1 1],'Visible','off');
         ax2 = axes('Position',[.3 .1 .6 .8]);

        
         
       
         plot(ax2,xid,SPM,'b-o',xid,BaseLine,'r-o',xid,actual,'g-o','LineWidth',1.2);
         grid on
         
         
          

        
     
        hold on
       
         %draw the division line
        l = line(length(DataLength)-1-PredictionLength*[1 1], get(gca, 'ylim'));
        set(l, 'color', [0,0,0],'LineWidth',1.2);
        PM25Legend=legend('SPM Prediction','BaseLine Prediction','Actual PM2.5','Start 1Hour Prediction','East')
        legend('boxoff')
        %set legend position
        pos = get(PM25Legend,'position');
        set(PM25Legend, 'position',[0 0.2 pos(3:4)])
           
        descr = {'PM2.5 Data of Device :';
        files(fileIndex).name;
        '  ';
        'RMSE of SPM: ';
        num2str(RMSE_SPM);
        ' ';
        'RMSE of BaseLine: ';
        num2str(RMSE_BaseLine);
        };
     
      
        
        axes(ax1) % sets ax1 to current axes
        
        %set(gcf,'Visible','off')              % turns current figure "off"
        
        text(.025,0.6,descr)
        
        
        
   
        
        
        hold off




       
       



        
      
  
        
        
        %reset csv fileDir 
       fileDir='';
       fileDir=strcat('./',accessMeasurement);
       fileDir=strcat(fileDir,'/');
      
       
        %save output as png image in the accessMeasurement folder
        outputFilename=strcat(accessMeasurement,'_');
        outputFilename=strcat(outputFilename,files(fileIndex).name);
        outputFilename=strcat(outputFilename,'.png');
        outputFilename=strcat(fileDir,outputFilename);
        
        saveas(gcf,outputFilename);



       



       

end
csv2fft=0;
%%%%
