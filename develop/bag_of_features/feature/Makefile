feature.so: feature.o
	g++ -shared -o feature.so feature.o `pkg-config --libs opencv`

feature.o: feature.cpp
	g++ -Wall -fPIC -c feature.cpp -I/usr/local/include/python2.7
