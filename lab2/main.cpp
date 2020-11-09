#include <iostream>
#include <fstream>
#include <string_view>
#include <string>
#include <iterator>
#include <algorithm>
#include <functional>
#include <map>

size_t SIZE = 32768;

//VERY strongly depends on pyrandbits file (should contain 32768 lines and each line contains a number mod(2^64)
void PyRandToPlainArr(std::string_view path_in, uint64_t* PlainArr) 
{

	std::fstream in_stream(path_in.data());
	std::string buf(20,'a');
	for(size_t i = 0; i < SIZE; ++i)
	{
		getline(in_stream, buf);
		PlainArr[i] = std::stoull(buf,0,10);
		
	}
	
	in_stream.close();
}

double CharacterUniformityCriteria_1(uint64_t* stats, double alfa)
{
    
    double freqArr[256] = {};

	for(size_t i = 0; i < SIZE; ++i)
	{
		for(size_t j = 0; j < 8; ++j)
		{
			++freqArr[((stats[i] >> (8*j)) & 0b11111111)];			
		}
	}


	double X2 = 0.0;
	for(size_t i = 0; i < 256; ++i)
	{
		X2 += ( ( (freqArr[i] - 1024.0)*(freqArr[i] - 1024.0)  ) / (1024.0)   );
	}

	return X2;
}

double CharacterIndependencyCriteria_2(uint64_t* stats, double alfa)
{

	float freqArr[256+1][256+1] = {}; //declare and init with 0

    for(size_t i = 0; i < SIZE; ++i)
	{
	   	++freqArr[    stats[i] & 0b11111111    ][  (stats[i] >> 8) & 0b11111111   ];
		++freqArr[    (stats[i] >> 16) & 0b11111111    ][ (stats[i] >> 24) & 0b11111111    ];
		++freqArr[    (stats[i] >> 32) & 0b11111111    ][ (stats[i] >> 40) & 0b11111111    ];
		++freqArr[    (stats[i] >> 48) & 0b11111111    ][ (stats[i] >> 56) & 0b11111111    ];
	}

	for(size_t i = 0; i < 256; ++i)
	{
		for(size_t j = 0; j < 256; ++j)
		{
			freqArr[i][256] += freqArr[i][j];
			freqArr[256][j] += freqArr[i][j];
		}
	}

	float X2 = 0.0;
	float temp1;
	float temp2;
	
	for(size_t i = 0; i < 255; ++i)
	{
		for(size_t j = 0; j < 255; ++j)
		{
		    if((freqArr[i][j] != 0) && ((freqArr[256][i] * freqArr[j][256]) != 0) )
		    {
			    X2 +=  ( ( freqArr[i][j] * freqArr[i][j] ) / ( freqArr[256][i] * freqArr[j][256] )) ;
			//    std::cout << "zn cr2  " << freqArr[256][i] * freqArr[j][256] << std::endl;
			}
		}
	}	
	--X2;
	X2 = X2 * 131072;// 4.0 ne 8.0
    	
	 
	return X2;
}



double CharacterHomoCriteria_3(uint64_t* stats, double alfa)
{
    double X2 = 0.0;
    double freqArr[16+1][256] = {}; // here can be 256+1, but we already know that length of interval is 2048*8

    for(size_t i = 0; i < 16; ++i)
    {
        for(size_t j = 0; j < 2048; ++j)
        {
            for(size_t k = 0; k < 8; ++k)
            {
                ++freqArr[i][((stats[i*2048 + j] >> (8*k)) & 0b11111111)];
            }
        }     
    }

    for(size_t i = 0; i < 16; ++i)
    {
        for(size_t j = 0; j < 256; ++j)
        {
            freqArr[16][j] += freqArr[i][j];
        }
    }


    for(size_t i = 0; i < 16; ++i)
    {
        for(size_t j = 0; j < 256; ++j)
        {
            if(freqArr[16][j] != 0)
            {
                X2 += ( ( (double)(freqArr[i][j]) * (double)(freqArr[i][j]) ) / ((double)freqArr[16][j] * (SIZE/2)) );
            }
        }        
    }
    --X2;
    X2 = X2 * SIZE * 8.0;//4.0 or 8.0

	return X2;
}
void ArrangeCSV(std::string_view path_in, std::string_view pathCSV, uint64_t* stats)
{
    std::ofstream CSVStream(pathCSV.data());
    
    std::function<double(uint64_t*, double)> criteriaArray[3] = {};
    criteriaArray[0] = CharacterUniformityCriteria_1;
    criteriaArray[1] = CharacterIndependencyCriteria_2;
    criteriaArray[2] = CharacterHomoCriteria_3;

    std::pair<std::string, std::function<void(std::string_view, uint64_t*)>> too( "Crypto.Random.random", PyRandToPlainArr);

    const double alfaArray[3] = { 0.01, 0.05, 0.1};
    const double theoreticAlfaArray[3][3] = { { 307.618808424, 292.149330411, 281.648151906}, {65863.93, 65618.17, 65487.15}, 
                                              {4027.91713, 3951.8232 , 3928.20785 }};


   


                                  
    							
	double mark = 0.0;
    for(size_t k = 0; k < 3; ++k)
    {
	    CSVStream << "generator_type" << ",     " << "alfa" << ",       " << theoreticAlfaArray[0][k] << ",,     " <<
	                                                                         theoreticAlfaArray[1][k] << ",,     " <<
	                                                                         theoreticAlfaArray[2][k] << ",     " << '\n';
        
            too.second(path_in, stats);
            CSVStream << too.first << ",     " << alfaArray[k] << ",     ";
         
            for(size_t j = 0; j < 3; ++j)
            {
               // CSVStream <<  criteriaArray[j](stats, alfaArray[k]) << ",     ";
               mark = criteriaArray[j](stats, alfaArray[k]);
               CSVStream << mark << ",   ";
           
                if(mark>theoreticAlfaArray[j][k])
                      {
                   CSVStream << "Fail,  ";
                }
                  else 
                     {
                       CSVStream << "PASS,  ";
                  }
             }
   
            CSVStream <<  "\n";
        
        CSVStream << "\n\n";
      
        std::cout << "DONE, check result.csv please" << std::endl;
        
    }

    CSVStream.close();
}


int main()
{
	std::string_view path_csv("/home/ftl/KuLab1/grades.csv");
	std::string_view path_in("/home/ftl/KuLab1/pyrandbits");

	uint64_t* PlainArr = new uint64_t[SIZE]{}; 
	PyRandToPlainArr(path_in, PlainArr);

	ArrangeCSV(path_in, path_csv, PlainArr);
	delete[]PlainArr;
return 0;
}
