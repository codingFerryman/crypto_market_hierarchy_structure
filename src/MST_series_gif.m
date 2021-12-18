files = dir('*.png');
FileName = 'MST_series';
for j=1:length(files)
    image = imread([num2str(j) '.png'], 'BackgroundColor',[1 1 1]); 
    [A,map] = rgb2ind(image,256);
    if (j==1)
        imwrite(A,map,[FileName '.gif'],'gif','LoopCount',Inf,'DelayTime',1);
    else
        imwrite(A,map,[FileName '.gif'],'gif','WriteMode','append','DelayTime',1);
    end
end