dirpath <- paste0("/home/", Sys.getenv("UNAME"))
version <- names(read.csv(paste0(dirpath,"/env.version.tmp")))
length_str <- nchar(version)
version <- substr(version, 2,length_str)
filepath <- paste0(dirpath, "/R/omiq_v", version, "/OmiqPipeline")
install.packages(filepath, repos=NULL, type="source")

