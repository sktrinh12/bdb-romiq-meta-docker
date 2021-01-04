args <- commandArgs(trailingOnly=TRUE)
rerun_rd <- FALSE

# test if there is one argument
if (length(args) == 0) {
    stop("At least one argument must be supplied (timestamp).n", call.=FALSE)
} else if (length(args) == 2) {
    if (match(tolower(args[2]), "true") | tolower(args[2]) == "t") { 
        rerun_rd <- TRUE
    }
}

print(R.Version())
print(paste(rep("+",25), collapse=''))
print(paste0("the arguments: ", args))
