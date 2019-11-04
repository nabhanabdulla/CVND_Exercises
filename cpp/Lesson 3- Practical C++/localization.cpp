#include<iostream>
#include<vector>
#include<string>

using namespace std;

vector <float> sense(vector<float> p, string Z);
vector <float> move(vector<float> p, int U);
int print_float_vector(vector<float> v);
int print_string_vector(vector<string> v);

vector <float> p = {0.2, 0.2, 0.2, 0.2, 0.2};
vector <string> world = {"green", "red", "red", "green", "green"};
vector <string> measurements = {"red", "green"};
vector <int> motions = {1,1};

float pHit = 0.6;
float pMiss = 0.2;
float pExact = 0.8;
float pOvershoot = 0.1;
float pUndershoot = 0.1;

int main(){
    cout << "Starting localization... " << endl;
    cout << "The environment is ..." << endl;
    print_string_vector(world);

    cout << "Initial Belief ... " << endl;
    print_float_vector(p);

    for(int i=0; i < measurements.size(); i++){
        cout << "Sensing...  ";
        cout << measurements[i] << endl;
        p = sense(p, measurements[i]);
        print_float_vector(p);

        cout << "Moving...  ";
        cout << motions[i] << " step right" << endl;
        p = move(p, motions[i]);
        print_float_vector(p);

    }


    return 0;
}

int print_float_vector(vector<float> v){
    for(int i=0; i < v.size(); i++){
        cout << v[i] << " ";
    }
    cout << endl;

    return 0;
}

int print_string_vector(vector<string> v){
    for(int i=0; i < v.size(); i++){
        cout << v[i] << " ";
    }
    cout << endl;

    return 0;
}

vector <float> sense(vector<float> p, string Z){
    vector <float> q;
    float s = 0;

    for(int i=0; i < p.size(); i++){
        float hit;
        if (Z == world[i]){
            hit = 1;
        }
        else{
            hit = 0;
        }

        float new_confidence = p[i] * (hit * pHit + (1 - hit) * pMiss);
        q.push_back(new_confidence);

        s += new_confidence;
    }

    for(int j=0; j < q.size(); j++){
        q[j] = q[j] / s;
    }

    return q;
}

vector <float> move(vector<float> p, int U){
    vector <float> q;
    float s = 0;
    int len_p = p.size();

    for(int i=0; i < len_p; i++){
        s = pExact * p[(i - U) % len_p];
        s += pOvershoot * p[(i-U-1) % p.size()];
        s += pUndershoot * p[(i-U+1) % p.size()];

        q.push_back(s);
    }

    return q;
}