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
int gcd(int a, int b){ if (!b) return a; return gcd(b,a%b);}
ll gcd(ll a, ll b){ if (!b) return a; return gcd(b,a%b);}

int to[1000010][26],K=1,cnt[1000010],T,fail[1000010],pnod[120],root=1;
int q[1000010];

//do K=1, root=1-root
int ins(int &nod, int p, string &s){
	if (nod==0) nod=++K;
	
	if (p==s.length())
		return nod;
	
	return ins(to[nod][s[p]-'a'],p+1,s);
}

void calc_fail(){
	T=1,q[1]=root;
	fail[root]=root;
	
	int i,j;
	for (i=1; i<=T; i++){
		int cr=q[i];
		
		for (j=0; j<26; j++)
			if (to[cr][j]!=0){
				int nxt=to[cr][j];
				
				int f=fail[cr];
				while (f!=1 && to[f][j]==0)
					f=fail[f];
				
				fail[nxt]=f;
				if (to[f][j]!=0 && to[f][j]!=nxt)
					fail[nxt]=to[f][j];
					
				
				q[++T]=nxt;
				
			}
	}
}

void prop(){
	for (int i=K; i>1; i--){
		cnt[fail[q[i]]]+=cnt[q[i]];
	}
}

string s,a;
int N;

int main(){
	
	ifstream fin("ahocorasick.in");
	ofstream fout("ahocorasick.out");
	fin >> s;
	
	int i;
	fin >> N;
	
	
	
	for (i=1; i<=N; i++){
		fin >> a;
		pnod[i]=ins(root,0,a);
	}
	
	ld var = sqrt(45);
	ios::sync_with_stdio(0);

	calc_fail();

	int cr=1;
	for (i=0; i<s.length(); i++){
		while (cr!=1 && to[cr][s[i]-'a']==0)
			cr=fail[cr];
			
		if (to[cr][s[i]-'a']!=0)
			cr=to[cr][s[i]-'a'];
		
		cnt[cr]++;
	}
	
	
	prop();
	
	for (i=1; i<=N; i++)
		fout << cnt[pnod[i]] << "\n";
	
	return 0;
}
