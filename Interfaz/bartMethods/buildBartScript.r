library("bartMachine")
library("caTools")
library("optparse")

sink("D:\\Escritorio\\Codigo\\Tesis\\Interfaz\\bartMethods\\summary.txt", append = FALSE)

option_list = list(
    make_option(c("-f", "--file"), type="character", default="",
            help="Path of the dataset", metavar="character"),
    make_option(c("-v", "--crossValidate"), type="integer", default=FALSE,
            help="Cross validate the model", metavar="integer"), 
    make_option(c("-r", "--response"), type="character", default="",
            help="Name of the response variable", metavar="character"),
    make_option(c("-n", "--numTrees"), type="integer", default=200,
            help="Number of trees", metavar="integer"),
    make_option(c("-i", "--burnIn"), type="integer", default=100,
            help="Number of burn in iterations", metavar="integer"),
    make_option(c("-l", "--postBurnIn"), type="integer", default=100,
            help="Number of post burn in iterations", metavar="integer"),
    make_option(c("-a", "--alpha"), type="numeric", default=0.95,
            help="Alpha value", metavar="numeric"),
    make_option(c("-b", "--beta"), type="numeric", default=2,
            help="Beta value", metavar="numeric"),
     make_option(c("-k", "--kVar"), type="numeric", default=2,
                     help="Prior probability", metavar="numeric"),
    make_option(c("-q", "--quantiles"), type="numeric", default=0.5,
            help="Quantile of the prior on the error variance at which the data-based estimate is
placed", metavar="numeric"),
    make_option(c("-u", "--nu"), type="numeric", default=3,
            help="Degrees of freedom for x^2 prior", metavar="numeric"),
    make_option(c("-g", "--grow"), type="numeric", default=1,
            help="Grow percentage for MH", metavar="numeric"),
    make_option(c("-p", "--prune"), type="numeric", default=1,
            help="Prune percentage for MH", metavar="numeric"),
    make_option(c("-c", "--change"), type="numeric", default=1,
            help="Change percentage for MH", metavar="numeric")
    )

opt_parser = OptionParser(option_list=option_list, add_help_option=FALSE)
opt = parse_args(opt_parser)

df = read.csv(opt$file, header=TRUE, sep=",")
# Split data
print(opt$response)
split = sample.split(df[, opt$response], SplitRatio = 0.8)
train = subset(df, split == TRUE)
test = subset(df, split == FALSE)

# Train model
if(opt$crossValidate == TRUE){
        bart = build_bart_machine_cv(X = train[, -which(names(train) == opt$response)],
                                        y = train[, opt$response])

} else {
        bart = build_bart_machine(X = train[, -which(names(train) == opt$response)],
                                y = train[, opt$response],
                                num_trees = opt$numTrees,
                                num_burn_in = opt$burnIn,
                                num_iterations_after_burn_in = opt$postBurnIn,
                                alpha = opt$alpha,
                                beta = opt$beta,
                                k = opt$k,
                                q = opt$quantiles,
                                nu = opt$nu)
                                # TODO: Ver como convertir esto en un parametro
                                #mh_prob_steps = c(as.numericopt$grow, opt$prune, opt$change))
}

summary(bart)
sink()