package test;


import java.io.File;
import java.util.*;

import localsearch.domainspecific.vehiclerouting.vrp.ConstraintSystemVR;
import localsearch.domainspecific.vehiclerouting.vrp.IFunctionVR;
import localsearch.domainspecific.vehiclerouting.vrp.VRManager;
import localsearch.domainspecific.vehiclerouting.vrp.VarRoutesVR;
import localsearch.domainspecific.vehiclerouting.vrp.constraints.Implicate;
import localsearch.domainspecific.vehiclerouting.vrp.constraints.eq.Eq;
import localsearch.domainspecific.vehiclerouting.vrp.constraints.leq.Leq;
import localsearch.domainspecific.vehiclerouting.vrp.entities.ArcWeightsManager;
import localsearch.domainspecific.vehiclerouting.vrp.entities.NodeWeightsManager;
import localsearch.domainspecific.vehiclerouting.vrp.entities.Point;
import localsearch.domainspecific.vehiclerouting.vrp.functions.AccumulatedEdgeWeightsOnPathVR;
import localsearch.domainspecific.vehiclerouting.vrp.functions.AccumulatedNodeWeightsOnPathVR;
import localsearch.domainspecific.vehiclerouting.vrp.functions.IndexOnRoute;
import localsearch.domainspecific.vehiclerouting.vrp.functions.LexMultiFunctions;
import localsearch.domainspecific.vehiclerouting.vrp.functions.RouteIndex;
import localsearch.domainspecific.vehiclerouting.vrp.functions.TotalCostVR;
import localsearch.domainspecific.vehiclerouting.vrp.invariants.AccumulatedWeightEdgesVR;
import localsearch.domainspecific.vehiclerouting.vrp.invariants.AccumulatedWeightNodesVR;

public class HeuristicOnePoint {
    int N, M, K; // N khach M goi hang
    int[] q;	 // khoi luong hang tai diem
    int[] Q;	 // khoi luong max cua xe
    int[][] d; 	 // distance

    ArrayList<Point> start;
    ArrayList<Point> end;
    ArrayList<Point> clientPoints;    	// tat ca cac diem phuc vu 2N+2M = all point \ 2K  diem 0 
    
    
    ArrayList<Point> allPoints;        	// tinh ca 2 diem gia
    
    NodeWeightsManager clMng;
    NodeWeightsManager pkMng;
    ArcWeightsManager weightsMng;    	// luu tru trong so tren canh noi giua cac point

    NodeWeightsManager maxWMng;
    
    HashMap<Point, Integer> mapPoint2ID;
    HashMap<Integer, Point> reverseMapPoint2ID;

    // modelling
    VRManager mgr;
    VarRoutesVR XR; // bien loi giai (luu tap cac route)
    ConstraintSystemVR CS;
    LexMultiFunctions F;
    IFunctionVR obj;
    IFunctionVR[] d1; 
    IFunctionVR[] d2; // danh co thiet lap rang buoc cho tat ca cac diem
    IFunctionVR[] d3; // danh co thiet lap rang buoc ve truoc sau
    IFunctionVR[] d4; // danh co thiet lap rang buoc dung diem lay va tra
    IFunctionVR[] cost; // cost[k] la chieu dai cua route thu k
    Random R = new Random();
    
    

    
    public ConstraintSystemVR getCS() {
		return CS;
	}

	public IFunctionVR getObj() {
		return obj;
	}


	public IFunctionVR[] getCost() {
		return cost;
	}

	public VarRoutesVR getXR() {
		return XR;
	}

	public void readData(String fn) {
        try {
            Scanner in = new Scanner(new File(fn));
            N = in.nextInt();
            M = in.nextInt();
            K = in.nextInt();
//            K=1;

            q = new int[M + 1];
            Q = new int[K + 1];
            d = new int[2 * N + 2 * M + 1][2 * N + 2 * M + 1];

            for (int i = 1; i <= M; i++) {
                q[i] = in.nextInt();
            }
            for (int i = 1; i <= K; i++) {
                Q[i] = in.nextInt();
            }
            for (int i = 0; i <= 2 * N + 2 * M; i++) {
                for (int j = 0; j <= 2 * N + 2 * M; j++) {
                    d[i][j] = in.nextInt();
                }
            }
            in.close();
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    public void printReadData() {
        System.out.println(N + " " + M + " " + K);
        for (int i = 1; i <= M; i++) {
            System.out.print(q[i] + " ");
        }
        System.out.println();
        for (int i = 1; i <= K; i++) {
            System.out.print(Q[i] + " ");
        }
        System.out.println();
        for (int i = 0; i <= 2 * N + 2 * M; i++) {
            for (int j = 0; j <= 2 * N + 2 * M; j++) {
                System.out.print(d[i][j] + " ");
            }
            System.out.println();
        }
    }

    public void mapping() {
        start = new ArrayList<Point>();
        end = new ArrayList<Point>();
        clientPoints = new ArrayList<Point>();
        allPoints = new ArrayList<Point>();
        mapPoint2ID = new HashMap<Point, Integer>();
        reverseMapPoint2ID = new HashMap< Integer,Point>();

       
        // khoi tao cac diem bat dau va ket thuc cua cac xe (route)
        for (int k = 1; k <= K; k++) {
            // them 2 k diem gia
            Point s = new Point(0);
            Point t = new Point(0);
            start.add(s);
            end.add(t);
            allPoints.add(s);
            allPoints.add(t);

            mapPoint2ID.put(s, 0);
            mapPoint2ID.put(t, 0);
            reverseMapPoint2ID.put(0, s);
            reverseMapPoint2ID.put(0, t);
        }


        for (int i = 1; i <= 2 * N + 2 * M; i++) {
            Point p = new Point(i);
            clientPoints.add(p);
            allPoints.add(p);
            mapPoint2ID.put(p, i);
            reverseMapPoint2ID.put(i,p);
        }

        clMng = new NodeWeightsManager(allPoints);
        pkMng = new NodeWeightsManager(allPoints);
        
        maxWMng=new NodeWeightsManager(allPoints);
        
        weightsMng = new ArcWeightsManager(allPoints);

        // set trong so duong di
        for (Point p : allPoints){
            for (Point q : allPoints) {
                int ip = mapPoint2ID.get(p);
                int iq = mapPoint2ID.get(q);
                weightsMng.setWeight(p, q, d[ip][iq]);
            }
        }

        // set trong so tai moi node (node person hoac pack)
        // rang buoc tra hang voi khach thi throng so am di, khong co lien quan thi trong so = 0
        
        for (int i = 0; i < K; i++) {
            Point s = start.get(i);
            Point t = end.get(i);
//            System.out.println(s.toString());
            maxWMng.setWeight(s, Q[i+1]);
            maxWMng.setWeight(t, Q[i+1]);
        }

        
        
        for (Point p : clientPoints){
            clMng.setWeight(p, 0);
            pkMng.setWeight(p, 0);
            int tmp = mapPoint2ID.get(p);
//            if(tmp == 0) { 
//            	
//            	continue;
//            }
////            for (int i=0;i<K;i++) {
            maxWMng.setWeight(p, 0);

            
            if (tmp <= N) {
                clMng.setWeight(p, 1);        
            } else if (tmp <= N + M) {
                pkMng.setWeight(p, q[tmp-N]);
            } else if (tmp <= 2 * N + M) {
                clMng.setWeight(p, -1);
            } else if (tmp <= 2 * N + 2 * M) {
                pkMng.setWeight(p, -q[tmp-N-M-N]);
            }
        }
    }

    public void stateModel2(){
        mgr = new VRManager();
        XR = new VarRoutesVR(mgr);
        // cac phuong an se dc dem tu 0
        for (int i = 0; i < start.size(); i++) {
            Point s = start.get(i);
            Point t = end.get(i);
            XR.addRoute(s, t);
        }
        // add co the di qua
        for (Point p : clientPoints) {
            XR.addClientPoint(p);// khai bao XR co the se di qua diem p
        }
        // thiet lap rang buoc
        CS = new ConstraintSystemVR(mgr);

        AccumulatedWeightNodesVR personAccum = new AccumulatedWeightNodesVR(XR, clMng);
        AccumulatedWeightNodesVR packAccum = new AccumulatedWeightNodesVR(XR, pkMng);
//        AccumulatedWeightEdgesVR weightAccum = new AccumulatedWeightEdgesVR(XR, weightsMng);

        AccumulatedWeightNodesVR maxAccum = new AccumulatedWeightNodesVR(XR,maxWMng);
        
        d1 = new IFunctionVR[2 * N + 2 * M + 2 * K + 2];
        d2 = new IFunctionVR[2 * N + 2 * M + 2 * K + 2];
        for (Point p : allPoints) {
            int tmp = mapPoint2ID.get(p);
            if(tmp == 0) continue;
            // rang buoc tai trong
//            d2[tmp] = new AccumulatedNodeWeightsOnPathVR(packAccum, p);

            // trong luong toi da cua xe ma diem p thuoc ve
//            for(int k=0;k<K;k++) {
                
//                d1[tmp]=new RouteIndex(XR, p);
                  // neu p thuoc k 
            d1[tmp] = new AccumulatedNodeWeightsOnPathVR(maxAccum, p);
            d2[tmp] = new AccumulatedNodeWeightsOnPathVR(packAccum, p);
//                CS.post(new Implicate(new Eq(d1[tmp], k),new Leq(d2[tmp], Q[k])));
            CS.post(new  Leq(d2[tmp], d1[tmp]));

//            }
//            
//            d2[tmp] = new AccumulatedNodeWeightsOnPathVR(packAccum, p);
//            CS.post(new Leq(d2[tmp],6));
//            CS.post(new Leq(0, d2[tmp]));

            // rang buoc so nguoi
            d2[tmp] = new AccumulatedNodeWeightsOnPathVR(personAccum, p);
            CS.post(new Leq(d2[tmp], 1));
//            CS.post(new Leq(0, d2[tmp]));
        }

        // xet tat ca cac diem thi phai co diem nhan roi thi moi duoc tra
        d3 = new IFunctionVR[2 * N + 2 * M + 2 * K + 10];
        for (Point p : allPoints) {
            int tmp = mapPoint2ID.get(p);
            if (tmp == 0)
                continue;
            if (tmp <= N + M) { // thay vi dung cai nay co the dung service point
                Point pTo = reverseMapPoint2ID.get(tmp + N + M);
                d3[tmp] = new IndexOnRoute(XR, p);
                d3[tmp + N + M] = new IndexOnRoute(XR, pTo);
                CS.post(new Leq(d3[tmp], d3[tmp + N + M]));
            }
        }

        // rang buoc phai trả dung diem len va xuong
        d4 = new IFunctionVR[2 * N + 2 * M + 2 * K + 10];
        for (Point p : allPoints) {
            int tmp = mapPoint2ID.get(p);
            if (tmp == 0)
                continue;
            if (tmp <= N + M) {
                Point pTo = reverseMapPoint2ID.get(tmp + N + M);
                d4[tmp] = new RouteIndex(XR, p);
                d4[tmp + N + M] = new RouteIndex(XR, pTo);
                CS.post(new Eq(d4[tmp], d4[tmp + N + M]));
            }
        }
        // neu muon in tung cai 
//        cost = new IFunctionVR[K];
//        for (int k = 1; k <= K; k++) {
//            Point tk = XR.endPoint(k);
//            cost[k - 1] = new AccumulatedEdgeWeightsOnPathVR(weightAccum, tk);
//        }

        obj = new TotalCostVR(XR, weightsMng);// tong khoang cach di chuyen cua K xe (route)
        mgr.close();
    }

    public void initialSolution() {
        ArrayList<Point> listPoints = new ArrayList<Point>();
        for (int k = 1; k <= XR.getNbRoutes(); k++) {
            listPoints.add(XR.startPoint(k));
        }
        for (Point p : clientPoints) {
            Point x = listPoints.get(R.nextInt(listPoints.size()));
            mgr.performAddOnePoint(p, x);
            listPoints.add(p);
        }
//        System.out.println("Init Router \n"+XR.toString() + "violations = " + CS.violations() + ", cost = " + obj.getValue());

    }

    class Move {
        Point x;
        Point y;
        public Move(Point x, Point y) {
            this.x = x;
            this.y = y;
        }
    }

    public void exploreNeighborhood(ArrayList<Move> cand) {
        cand.clear();
        int minDeltaC = Integer.MAX_VALUE;
        double minDeltaF = minDeltaC;
        for (int k = 1; k <= XR.getNbRoutes(); k++) {
            for (Point y = XR.next(XR.startPoint(k)); y != XR.endPoint(k); y = XR.next(y)) {
                for (Point x : clientPoints)
                    if (x != y && x != XR.next(y)) {
                        int deltaC = CS.evaluateOnePointMove(x, y);
                        double deltaF = obj.evaluateOnePointMove(x, y);
//                        System.out.print(deltaC + "_" + (int)deltaF + " |");
                        if (!(deltaC < 0 || (deltaC == 0 && deltaF < 0)))
                            continue;
                        if (deltaC < minDeltaC || (deltaC == minDeltaC && deltaF < minDeltaF)) {
                            cand.clear();
                            cand.add(new Move(x, y));
                            minDeltaC = deltaC;
                            minDeltaF = deltaF;
                        } else if (deltaC == minDeltaC && deltaF == minDeltaF)
                            cand.add(new Move(x, y));
                    }
            }
        }
    }

    public void search(int maxIter) {
        initialSolution();
        int it = 0;
        ArrayList<Move> cand = new ArrayList<Move>();
        while (it < maxIter) {
            exploreNeighborhood(cand);
            if (cand.size() <= 0) {
//                System.out.println("Reach local optimum");
                break;
            }
            Move m = cand.get(R.nextInt(cand.size()));
            mgr.performOnePointMove(m.x, m.y);
//            System.out.println("\nStep " + it + ", XR   " + m.x.getID() + ","+m.y.getID() +"\n" + XR.toString() + "violations = " + CS.violations()
//            + ", cost = " + obj.getValue()+ "");
            it++;
        }
        
    

    }


    public static void main(String[] args) {
        HeuristicOnePoint A = new HeuristicOnePoint();

        A.readData("data.txt");
        double best = Integer.MAX_VALUE;
        int numberTry = 600;
        List<VarRoutesVR> resRoutesVR=new ArrayList<>();
        for (int i = 0; i < numberTry; i++) {
            A.mapping();
            A.stateModel2();
            A.search(10000);
            double cost = A.getObj().getValue();
            int vio =A.getCS().violations();
//            System.out.println("cost=" +cost+" violation="+vio );
          
            if (best > cost && vio==0) {
            	resRoutesVR.clear();
            	System.out.println("update");
                best = cost;
                resRoutesVR.add(A.getXR());
            }else if (best==cost){
            	resRoutesVR.add(A.getXR());
            }
            
        }
        System.out.println("\nbest : " + best);
        resRoutesVR.stream().forEach(e-> System.out.println(e.toString()));
    }
}
