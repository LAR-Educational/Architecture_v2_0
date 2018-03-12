


setwd("/home/tozadore/Projects/Arch_2/Analysis/")
getwd()


library(ggplot2)
library(reshape2)

library(RColorBrewer)


default <- function() {
  
  plot = theme_bw() + theme(
    #legend.position="top",
    axis.title=element_text(size=14, colour="black"),
    strip.text=element_text(size=14, colour="black"),
    legend.title=element_text(size=14, colour="black"),
    legend.text=element_text(size=14, colour="black"),
    axis.text.x=element_text(size=14, colour="black"),
    axis.text.y=element_text(size=14, colour="black")
  )
  
  return(plot)
}


mydata2=read.csv("ideal.csv")

mydata=read.csv("all_noise.csv")

total = mydata[which(mydata$Noise_Level=="Noise"),]
total = rbind(total,mydata[which(mydata$Noise_Level=="Ideal"),])


mydata$Classifier_Approach =factor(x=mydata$Classifier_Approach, levels = c( "KNN_hst", "KNN_pxl", "MLP_hst", "MLP_pxl", "SVM_hst", "SVM_pxl", "ENS_hst", "ENS_pxl", "ENS_all" ))



total$Classifier_Approach =factor(x=total$Classifier_Approach, levels = c( "KNN_hst", "KNN_pxl", "MLP_hst", "MLP_pxl", "SVM_hst", "SVM_pxl", "ENS_hst", "ENS_pxl", "ENS_all" ))



mydata = mydata[-which(mydata$Noise_Level=="Noise"),]

mydata = mydata[-which(mydata$Noise_Level=="Ideal"),]

mydata$Noise_Level = factor(x=mydata$Noise_Level, levels = c("Light", "Medium","Heavy"))



ggplot(mydata, aes(Noise_Level, fill= Classifier_Approach, y=Accuracy )) +
  geom_bar(stat="identity", position="dodge", colour="white", width=0.75 ) +
  default()+
  #scale_fill_manual(values=c("skyblue1","purple1","royalblue","darkviolet"))+
  ylim(0,1)





ggplot(total, aes(Noise_Level, fill= Classifier_Approach, y=Accuracy )) +
  geom_bar(stat="identity", position="dodge", colour="white", width=0.75 ) +
  default()+
  #scale_fill_manual(values=c("skyblue1","purple1","royalblue","darkviolet"))+
  ylim(0,1)




# 
# ggplot(mydata, aes( Classifier_Approach, fill=Noise_Level, y=Accuracy )) +
#   geom_bar(stat="identity", position="dodge", colour="white", width=0.75 ) +
#   default()+
#   #scale_fill_manual(values=c("skyblue1","purple1","royalblue","darkviolet"))+
#   ylim(0,1)



ggplot(mydata2, aes( Classifier_Approach, fill=Noise_Level, y=Accuracy )) +
  geom_bar(stat="identity", position="dodge", colour="white", width=0.75 ) +
  default()+
  #scale_fill_manual(values=c("skyblue1","purple1","royalblue","darkviolet"))+
  ylim(0,1)



#mydata <- mydata[order(levels(mydata$Classifier) =  c("KNN", "MLP", "SVM", "ENS"))]




#levels(mydata$Classifier) =  c("KNN", "MLP", "SVM", "ENS")







