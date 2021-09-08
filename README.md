# Opt
midterm planning optimization

# Đề bài 
- Có N hành khách 1, 2, …, N và M gói hàng N+1,N+ 2, …, N+M. Hành khách (người) (hoặc gói hàng) i có điểm đón là i và điểm trả là i+ N + M (i = 1,2,…,2N+2M). 
- Mỗi gói hàng i có khối lượng qi (i=N+1,…,N+M)
- Có K taxi 1,…,K xuất phát từ điểm 0. Mỗi xe taxi k có thể vận chuyển cùng 1 lúc 1 hành khách và tối đa Qk khối lượng hàng (xếp vào cốp xe) (k=1,…,K)
- Biết rằng d(i,j) là khoảng cách từ điểm i đến điểm j (I,j=0,…,2N+2M)
- Hãy tính toán phương án vận chuyển sao cho tổng quãng đường di chuyển của các xe ngắn nhất


# Model 1 : CS

- solver : ortool 

- NM2 = 2N+2M
- L[s] = 0, s = NM2+1, …, NM2+K​      L : khoảng cách tích lũy
- W[s] = 0, s = NM2+1,… NM2+K​        W : Tải hiện tại
- P[s] = 0, s = NM2+1,… NM2+K​        P : người trên xe
- mark[NM2+i] = mark[NM2+K+i], i = 1, …, K​         mark : đánh dấu point thuộc xe nào
- X[i] != X[j], mọi i != j, i,j = 1,2,…, NM2+K​     X : Lời giải
- X[i] != i, với mọi  i = 1,2,…, NM2+K ​

- X[i] = j => mark[i] = mark[j], với mọi i = 1,…, NM2+K, j = 1,…, NM2+2K​
- X[i] = j => L[j] = L[i] + d(i,j), với mọi i = 1,…, NM2+K, j = 1,…, NM2+2K​
- L[i] > L[i-N-M] , i = N+M+1,... NM2
- P[i] <= 1, i = 1, ...NM2+2K
- W[k+N] <= c(k), k = 1,...NM2+2K ​

- X[i] = j => P[j] = P[i] + 1, với mọi i = 1,…, NM2+K, j = 1,…, N            --- W ==  
- X[i] = j => W[j] = W[i] + wj, với mọi i = 1,…, NM2+K, j = N+1,…, N+M​         --- P ==
- X[i] = j => P[j] = P[i] - 1, với mọi i = 1,…, NM2+K, j = N+M+1,…, 2N+M        --- W ==
- X[i] = j => W[j] = W[i] - wj, với mọi i = 1,…, NM2+K, j = 2N+M+1,…, NM2​      --- P ==

- Hàm mục tiêu: f = L[NM2+K+1] + … + L[NM2+2K]  min



# model 2 :  MIP

- solver : ortools
Ràng buộc:
- Tổng (X(i,j)) với j thuộc A+(i) = Tổng (X(j,i)) với j thuộc A-(i) = 1 với mọi i = 1,…,2(M+N)
- Tổng (X(i,j)) với j thuộc A+(i) = Tổng (X(j,i+K)) với j thuộc A-(i) = 1 với mọi i = 2(M+N)+1,…,2(M+N)+K
- Tổng (X(j,i)) với j thuộc A+(i) = Tổng (X(i+K,j)) với j thuộc A-(i) = 0 với mọi i = 2(M+N)+1,…,2(M+N)+K
- Z(i) = Z(i+M+N) với mọi i = 1,…,M+N
- M(1-X(i,j)) + Z(i) >= Z(j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + Z(j) >= Z(i), với mọi (i,j) thuộc A
- M(1-X(i,j)) + W_max(i) >= W_max(j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + W_max(j) >= W_max(i), với mọi (i,j) thuộc A
- M(1-X(i,j)) + L(j) >= L(i) + d(i,j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + L(i) + d(i,j) >= L(j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + P(j) >= P(i) + p(j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + P(i) + p(j) >= P(j), với mọi (i,j) thuộc A
- M(1-X(i,j)) + W(k,j) >= W(k,i) + q(j), với mọi (i,j) thuộc A, k = 1,…,K
- M(1-X(i,j)) + W(k,i) + q(j) >= W(k,j), với mọi (i,j) thuộc A, k = 1,…,K
- L(i+M+N) >= L(i) + d(i,i+M+N), i=1,…,M +N
- P(i) ≤ 1, với mọi thuộc B
- W(i) ≤ W_max(i), với mọi i thuộc B
- L(2(M+N)+k) = 0, với mọi k = 1,…,K
- P(2(M+N)+k) = 0, với mọi k = 1,…,K
- W(2(M+N)+k) = 0, với mọi k = 1,…,K
- W_max(2(M+N)+k) = Q(k), với mọi k = 1,…,K
- Z(k+N) = Z(k+K+N) = k, với mọi k = 1,…,K 

Hàm mục tiêu:
- Tổng (X(i,j)d(i,j)) với (i,j) thuộc A -> min
# model 3 : Heuristic

- solver : cbls-vr:  https://github.com/dungkhmt/planningoptimization

NM2 = 2N+2M
1. Biến  
- Thêm điểm 2K điểm logic  NM2+1..NM2+2K tham chiếu tới điểm 0 và các điểm cuối cùng từng xe lần lưt  

- X[i] : Điểm tiếp theo của i trên lộ trình  	i= 1..NM2        	X= 
- L[i] : khoảng cách tích lũy tới i          	i= 					L=
- W[i] : Tải hiện tại							i=					W=
- P[i] : người trên xe						i=					P={0,1}
- IR[i]: xe mà điểm đó thuộc vể 				i=					IR=1..K

2. Ràng buộc 
* khởi tạo
- ok	L[s] = 0, s = NM2+1, …, NM2+K​              	điểm bắt đầu thì khoảng cách bằng 0  
- ok	W[s] = 0, s = NM2+1,… NM2+K​        		   	Khối lượng ban đầu 
- ok	P[s] = 0, s = NM2+1,… NM2+K​       			Số người ban đầu 
- ok	IR[s]= IR[e] = điểm logic 0                 khởi tạo điểểm gốc 
- ok  khởi tạo đường đi ban đầu  


* cơ bản (tools hỗ trợ )
- ok	IR[NM2+i] = IR[NM2+K+i], i = 1, …, K​        								điểm đầu và điểm cuối trùng nhau 
- ok	X[i] != X[j], mọi i!=j, i,j = 1,2,…, NM2+K									không cùng tham chiểu tới ​
- ok	X[i] != i, với mọi  i = 1,2,…, NM2+K 										không quay lại chính nó ​
- ok	X[i] = j => IR[i] = IR[j], với mọi i = 1,…, NM2+K, j = 1,…, NM2+2K			điẻm tới của nó thì cùng route vứi nó ​
- ok	X[i] = j => L[j] = L[i] + d(i,j), với mọi i = 1,…, NM2+K, j = 1,…, NM2+2K   tính khoảng cách nếu đi tới điểm đó 

* đặc biệt 
​
- ok	L[i] > L[i-N-M] , i = N+M+1,... NM2											Điểm nhận phải sau điểm đón + trar dung khach dung hang  
- ok	P[i] <= 1, i = 1, ...NM2+2K													Số ngưười không vượt quá 1
- ok	W[k+N] <= c(k), k = 1,...NM2+2K 											Tải trọng hiện tại của xe khôgn được vượt quá ​

- ok	X[i] = j => P[j] = P[i] + 1, với mọi i = 1,…, NM2+K, j = 1,…, N             Đón ngưười thì chỉ trong 1..N
- ok	X[i] = j => W[j] = W[i] + w[j], với mọi i = 1,…, NM2+K, j = N+1,…, N+M​      Đón vật thì chỉ trong N+1..N+M
- ok	X[i] = j => P[j] = P[i] - 1, với mọi i = 1,…, NM2+K, j = N+M+1,…, 2N+M      Trả người 
- ok	X[i] = j => W[j] = W[i] - wj, với mọi i = 1,…, NM2+K, j = 2N+M+1,…, NM2​     Trả vật 
- 4 ràng buộc trên trong solver này thay bằng khưởi tạo trọng số âm cho node 


Hàm mục tiêu: thư vện hỗ trợ 
