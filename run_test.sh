for map in `find travis_test/test_files -mindepth 1 -name "*$1*"`
do
    echo "+-+-+ Map $map +-+-+"
        python3 main.py $map
done