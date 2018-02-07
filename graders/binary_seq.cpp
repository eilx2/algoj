#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <set>
#include <map>
#include <cmath>
#include <cstring>
#include <ctime>
#include <unordered_map>
#include <iomanip>
#include <complex>
#include <cassert>
using namespace std;

#define fi first
#define se second
#define pb push_back
#define all(v) (v).begin(),(v).end()
#define deb(a) cerr<< #a << "= " << (a)<<"\n";

typedef long long ll;
typedef unsigned long long ull;
typedef unsigned int uint;
typedef long double ld;
typedef complex<double> base;
typedef vector<int> vi;
typedef pair<int,int> pii;

template<class T> ostream& operator<<(ostream& stream, const vector<T> v){ stream << "[ "; for (int i=0; i<(int)v.size(); i++) stream << v[i] << " "; stream << "]"; return stream; }
ll fpow(ll x, ll p, ll m){ll r=1; for (;p;p>>=1){ if (p&1) r=r*x%m; x=x*x%m; } return r;}
ll inv(ll a, ll b){ return a<2 ? a : ((a-inv(b%a,a))*b+1)/a%b; }
int gcd(int a, int b){ if (!b) return a; return gcd(b,a%b);}
ll gcd(ll a, ll b){ if (!b) return a; return gcd(b,a%b);}

ll N,K,p[300000];

#define p (p+150000)

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	cin >> N >> K;
	
	ll i,cnt=0;
	for (i=0; i<=60; i++)
		if (N&(1ll<<i))
			p[i]=1,cnt++;
			
	if (cnt>K){
		cout << "No\n";
		return 0;
	}
	
	int cr=100;
	while (cnt<K){
		while (p[cr]==0) cr--;
		p[cr]--;
		p[cr-1]+=2;
		cnt++;
	}
	
	while (p[cr]==0) cr--;
	p[cr]+=p[cr-1]/2;
	cnt-=p[cr-1]/2;
	p[cr-1]%=2;
	
	
	for (i=-100; i<=100; i++)
		if (p[i]>0){
			cr=i;
			break;
		}
	
	if (cnt<K){
		p[cr]--;
		for (i=cr-1; i>=cr-(K-cnt); i--)
			p[i]=1;
		
		p[cr-(K-cnt)]++;
	}
	
	cout << "Yes\n";
	for (i=100; i>=-100000; i--)
		for (int j=1; j<=p[i]; j++)
			cout << i << " ";
	
	return 0;
}

