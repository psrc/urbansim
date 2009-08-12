empl<-list(employee="Anna",spouse="fred",children=3,child.ages=c(4,7,9))
for (i in 1:length(empl)) {
  cat(names(empl)[i]); cat(":")
  for (j in 1:length(empl[[i]])) {
    cat(unlist(empl[i])[j]); cat(" ")
  }
  cat("\n")
}
