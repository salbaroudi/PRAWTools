WORKPROJ="./WorkArea/"$1
OUTFOLD=$WORKPROJ"/"$2
CONFIG="./Templates/config.txt"
INFILE="./Templates/input.txt"
STARTSC="./ParchCodeBase/pstart.py"

echo $WORKPROJ
echo $OUTFOLD

mkdir $WORKPROJ
mkdir $OUTFOLD
cp $CONFIG $WORKPROJ
cp $STARTSC $WORKPROJ
cp $INFILE $WORKPROJ
