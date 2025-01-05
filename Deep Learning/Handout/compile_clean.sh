# complete compile the files
# Lecture number is given as the argument
# Compile all the modules separately
# Usage : go to the respective lecture folder and type the following command
# source ../compile_clean.sh #LectureNumber nonstopmode ref all-modules
#	nonstopmode will not stop compiling at warnings
#	ref will compile along with references
#	all-modules will generate pdf for all the modules 
#       #num_modules
if [[ "$2" == "nonstopmode" ]]; then
	pdflatex -interaction=nonstopmode -halt-on-error Lecture$1.tex
else
	pdflatex Lecture$1.tex
fi

if [[ $? == 1 ]]; then
	echo "Compilation is giving an error "
	return 1
fi

if [[ "$3" == "ref" ]]
then
	bibtex Lecture$1.aux
	pdflatex -interaction=nonstopmode Lecture$1.tex
	pdflatex -interaction=nonstopmode Lecture$1.tex
fi 

if [[ $? == 1 ]]; then
	echo "Could not link the references"
	return 1
fi
us="_"
if [[ "$4" == "all-modules" ]]; then
	for i in {1..9}
	do
		if [[ "$i" == "packages.tex" ]]; then
			continue
		fi
		cat modules/packages.tex modules/Module$i/Lecture$1$us$i.tex modules/end.tex > modules/temp.tex
		echo  "\end{document}"  >> modules/temp.tex
		pdflatex -interaction=nonstopmode modules/temp.tex

		if [[ "$3" == "ref" ]]
		then
			bibtex temp.aux
			pdflatex -interaction=nonstopmode modules/temp.tex
			pdflatex -interaction=nonstopmode modules/temp.tex
		fi
		mv temp.pdf modules/Module$i/Lecture$1_$i.pdf
	done
fi


echo "Deleting the generated logs"
rm modules/temp.tex
find . -name "*.nav" -type f -delete
find . -name "*.log" -type f -delete
find . -name "*.snm" -type f -delete
find . -name "*.aux" -type f -delete
find . -name "*.toc" -type f -delete
find . -name "*.out" -type f -delete
find . -name "*.bbl" -type f -delete
find . -name "*.blg" -type f -delete
