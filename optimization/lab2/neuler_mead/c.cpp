#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

#define n 2
#define alpha 1
#define beta 0.5
#define gamma 2
#define eps 1e-9

vector < vector < double > > points;

double f(vector<double>& args) {
    double x1 = args[0];
    double x2 = args[1];

    return 2*x1*x1 + x1*x2 + x2*x2 - 9*x1 - 5*x2;
}

bool compare(vector<double> x, vector<double> y) {
    return f(x) < f(y);
}

void get_xc(vector<double> * xc) {
    for (int i = 0; i < n; i++) { //coord loop
        double x = 0;
        for (int j = 0; j < n; j++) { //points loop
            x += points[j][i];
        }
        xc->push_back(x/n);
    }
}

void get_xr(vector<double> xc, vector<double> xh, vector<double> * xr) {
    for (int i = 0; i < n; i++) {
        xr->push_back((1+alpha)*xc[i] - alpha*xh[i]);
    }
}

void print_point(vector<double> point) {
    for (auto x : point) {
        cout << x << " ";
    }
    cout << "\b; f = "<< f(point);
    cout << endl;
}

void print_all() {
    cout << "----" << endl;
    for(auto point : points)  {
        print_point(point);
    }
    cout << "----" << endl;
}

int main() {
    // stage 1: select n+1 points
    for (int i = 0; i < n+1; i++) {
        vector<double> point;

        double x1, x2;
        cin >> x1 >> x2;

        point.push_back(x1); 
        point.push_back(x2);

        points.push_back(point);
    }

    while (true) {
        // stage 2: sort 
        sort(points.begin(), points.end(), compare);
        vector<double> xl = points[0]; // lowest
        vector<double> xs = points[1]; // second greatest
        vector<double> xh = points[2]; // greatest

        print_all();

        // stage 3: get centroid of first n points
        vector<double> xc;
        get_xc(&xc);
        
        // stage 4: reflect xh point from xc
        vector<double> xr;
        get_xr(xc, xh, &xr);
        print_point(xr);

        break;
    }
}