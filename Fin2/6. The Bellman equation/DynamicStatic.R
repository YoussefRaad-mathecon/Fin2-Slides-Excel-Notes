#source("DynamicStatic.R")

horizon<-30
u<-1.29
d<-0.85
R<-1.04
p<-0.5

E.beta<-function(beta) E.beta<-p*log(beta*(u-R)+R)+(1-p)*log(beta*(d-R)+R)

# gamma<-p*(u-r)/((p-1)*(d-r))
# beta.hat<-r*(1-gamma)/(gamma*(d-r)-(u-r))

beta.hat<-R*(p*u+(1-p)*d-R)/((u-R)*(R-d))

# a graphical check that we did the alegebra right
# x<--20:150/100
# plot(x,E.beta(x),type='l')
# abline(v=beta.hat)

IndirectUtility<-function(w) IndirectUtility<-log(w)+horizon*E.beta(beta.hat)

E.buyNhold <-function(alpha){
   E.buyNhold<-0
   for (i in 0:horizon){
      E.buyNhold<- E.buyNhold+dbinom(i,horizon,p)*log(alpha*u^i*d^(horizon-i)+(1-alpha)*R^horizon)
   }
   return(E.buyNhold)
}

y<-0:100/100

par(mfrow=c(1,1),adj=0.5)

plot(y,E.buyNhold(y)-horizon*E.beta(beta.hat),type='l',ylim=c(-0.3,0.1),xlab="fraction in stock, intitially",ylab="E(U(buy-and-hold)) - E(U(best fixed-fraction dynamic)) ")
abline(h=0,lty=2)

f<-exp(horizon*E.beta(beta.hat)-max(E.buyNhold(y)))-1
abline(v=y[which.max(E.buyNhold(y))])

