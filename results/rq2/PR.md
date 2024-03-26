The details of the 12 PRs are as follows:

### \#1 (PR was accepted)
+ Resource Type: dogfight_Z.dogLog.utils.JDBCConnection
+ Repository: [open-java](https://github.com/PointRider/open-java)
+ Pull Request: [pull\#2](https://github.com/PointRider/open-java/pull/2/commits/601f2e8a6a007b1fd575137423686fab82bec838)
+ File: dogfightZ/src/dogfight_Z/dogLog/dao/DBInit.java
  ```java
  public static void initDB() {
        JDBCConnection conn = JDBCFactory.takeJDBC();
        conn.submit(new Transaction() {
            @Override
            public boolean trying() {
                try {
                    for(String sql : ddl) {
                        conn.update(sql);
                    }
                } catch (SQLException e) {
                    e.printStackTrace();
                    return false;
                } 
                return true;
            }
        });
    }
  ```

### \#2 (PR was accepted)
+ Resource Type: java.net.URLClassLoader
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#3](https://github.com/Drun1baby/JavaSecurityLearning/pull/3/commits/fdce70c7848a8919dcdb893b55f5fb9a28e24741)
+ File: JavaSecurity/Reappearance/Serialable/src/DynamicClassLoader/URLClassLoader/JarRce.java
  ```java
      public static void main(String[] args) throws Exception{
        URLClassLoader urlClassLoader = new URLClassLoader(new URL[]{new URL("jar:file:///E:\\Calc.jar!/")});
        Class calc = urlClassLoader.loadClass("Calc");
        calc.newInstance();

    }
  ```
  
### \#3
+ Resource Type: java.util.Scanner
+ Repository: [level2and3](https://github.com/sumeet-malik/level2and3)
+ Pull Request: [pull\#3](https://github.com/sumeet-malik/level2and3/pull/3/commits/ec1c5b365f70116b2562853285bb3d5876eb4fe4)
+ File: Aug23/Codes/dp/Fib.java
  ```java
  public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scn = new Scanner(System.in);
		int n = scn.nextInt();
    //		int fn = fib(n);
    //		int[] strg = new int[n + 1];
    //		int fn = fibm(n, strg);
		int fn = fibt(n);
		System.out.println(fn);
	}
  ```

### \#4 (PR was accepted)
+ Resource Type: java.io.PrintWriter
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#3](https://github.com/Drun1baby/JavaSecurityLearning/pull/3/commits/7726285850e5e7d2670736fd1b0ec07a4a92b19c)
+ File: JavaSecurity/EL/BasicELVul/src/main/java/drunkbaby/basicelvul/HelloServlet.java
  ```java
     public void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        response.setContentType("text/html");
        // Hello
        PrintWriter out = response.getWriter();
        out.println("<html><body>");
        out.println("<h1>" + message + "</h1>");
        out.println("</body></html>");
    }
  ```
### \#5
+ Resource Type: java.util.Scanner
+ Repository: [SpringChallenge2022](https://github.com/CodinGame/SpringChallenge2022)
+ Pull Request: [pull\#29](https://github.com/CodinGame/SpringChallenge2022/pull/29/commits/3a4fddfdcbb7d15464b81620a72c64bf4b5908a0)
+ File: starterAIs/Starter.java
  ```java
     public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        // base_x,base_y: The corner of the map representing your base
        int baseX = in.nextInt();
        int baseY = in.nextInt();
        // heroesPerPlayer: Always 3
        int heroesPerPlayer = in.nextInt();     

        // game loop
        while (true) {
            int myHealth = in.nextInt(); // Your base health
            int myMana = in.nextInt(); // Ignore in the first league; Spend ten mana to cast a spell
            int oppHealth = in.nextInt();
            int oppMana = in.nextInt();
            int entityCount = in.nextInt(); // Amount of heros and monsters you can see
            
            List<Entity> myHeroes = new ArrayList<>(entityCount);
            List<Entity> oppHeroes = new ArrayList<>(entityCount);
            List<Entity> monsters = new ArrayList<>(entityCount);
            for (int i = 0; i < entityCount; i++) {
                int id = in.nextInt();              // Unique identifier      
                int type = in.nextInt();            // 0=monster, 1=your hero, 2=opponent hero        
                int x = in.nextInt();               // Position of this entity       
                int y = in.nextInt();
                int shieldLife = in.nextInt();      // Ignore for this league; Count down until shield spell fades      
                int isControlled = in.nextInt();    // Ignore for this league; Equals 1 when this entity is under a control spell        
                int health = in.nextInt();          // Remaining health of this monster      
                int vx = in.nextInt();              // Trajectory of this monster      
                int vy = in.nextInt();
                int nearBase = in.nextInt();        // 0=monster with no target yet, 1=monster targeting a base        
                int threatFor = in.nextInt();       // Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither       
                
                Entity entity = new Entity(
                    id, type, x, y, shieldLife, isControlled, health, vx, vy, nearBase, threatFor
                );
                switch (type) {
                    case TYPE_MONSTER:
                        monsters.add(entity);
                        break;
                    case TYPE_MY_HERO:
                        myHeroes.add(entity);
                        break;
                    case TYPE_OP_HERO:
                        oppHeroes.add(entity);
                        break;
                }                
            }

            for (int i = 0; i < heroesPerPlayer; i++) {
                Entity target = null;
                
                if (!monsters.isEmpty()) {
                    target = monsters.get(i % monsters.size());
                }

                if (target != null) {
                    System.out.println(String.format("MOVE %d %d", target.x , target.y));
                } else {
                    System.out.println("WAIT");
                }
            }
        }
    }
  ```

### \#6 (PR was accepted)
+ Resource Type: java.sql.Statement
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#4](https://github.com/Drun1baby/JavaSecurityLearning/pull/4/commits/866739eed18c74c7d04d4aac83f6650c0fdeda8d)
+ File: JavaSecurity/CodeReview/JavaSec-Code/MybatiSqli/src/main/java/com/drunkbaby/controller/SQLI.java
  ```java
   @RequestMapping("/jdbc/vuln")
    public String jdbc_sqli_vul(@RequestParam("username") String username) {

        StringBuilder result = new StringBuilder();

        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(url, user, password);

            if (!con.isClosed())
                System.out.println("Connect to database successfully.");

            // sqli vuln code
            Statement statement = con.createStatement();
            String sql = "select * from users where username = '" + username + "'";
            logger.info(sql);
            ResultSet rs = statement.executeQuery(sql);

            while (rs.next()) {
                String res_name = rs.getString("username");
                String res_pwd = rs.getString("password");
                String info = String.format("%s: %s\n", res_name, res_pwd);
                result.append(info);
                logger.info(info);
            }
            rs.close();
            con.close();


        } catch (ClassNotFoundException e) {
            logger.error("Sorry,can`t find the Driver!");
        } catch (SQLException e) {
            logger.error(e.toString());
        }
        return result.toString();
    }
  ```

### \#7 (PR was accepted)
+ Resource Type: java.sql.PreparedStatement
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#4](https://github.com/Drun1baby/JavaSecurityLearning/pull/4/commits/e86f052d9ce68069c3e91f9ec043352efe71167e)
+ File: JavaSecurity/CodeReview/JavaSec-Code/MybatiSqli/src/main/java/com/drunkbaby/controller/SQLI.java
  ```java
  @RequestMapping("/jdbc/sec")
    public String jdbc_sqli_sec(@RequestParam("username") String username) {

        StringBuilder result = new StringBuilder();
        try {
            Class.forName(driver);
            Connection con = DriverManager.getConnection(url, user, password);

            if (!con.isClosed())
                System.out.println("Connecting to Database successfully.");

            // fix code
            String sql = "select * from users where username = ?";
            PreparedStatement st = con.prepareStatement(sql);
            st.setString(1, username);

            logger.info(st.toString());  // sql after prepare statement
            ResultSet rs = st.executeQuery();

            while (rs.next()) {
                String res_name = rs.getString("username");
                String res_pwd = rs.getString("password");
                String info = String.format("%s: %s\n", res_name, res_pwd);
                result.append(info);
                logger.info(info);
            }

            rs.close();
            con.close();

        } catch (ClassNotFoundException e) {
            logger.error("Sorry, can`t find the Driver!");
            e.printStackTrace();
        } catch (SQLException e) {
            logger.error(e.toString());
        }
        return result.toString();
    }
  ```
  
### \#8
+ Resource Type: java.util.Scanner
+ Repository: [SpringChallenge2022](https://github.com/CodinGame/SpringChallenge2022)
+ Pull Request: [pull\#29](https://github.com/CodinGame/SpringChallenge2022/pull/29/commits/3a4fddfdcbb7d15464b81620a72c64bf4b5908a0)
+ File: config/level2/Boss.java
  ```java
      public static void main(String args[]) {
        Scanner in = new Scanner(System.in);
        int baseX = in.nextInt();
        int baseY = in.nextInt();
        int heroesPerPlayer = in.nextInt();

        int[] postX = baseX == 0 ? new int[] { 3000, 7000, 5500 } : new int[] { baseX - 3000, baseX - 7000, baseX - 5500 };
        int[] postY = baseY == 0 ? new int[] { 6500, 1500, 4000 } : new int[] { baseY - 6500, baseY - 1500, baseY - 4000 };

        // game loop
        while (true) {
            int myHealth = 0;
            int mana = 0;

            myHealth = in.nextInt();
            mana = in.nextInt();

            in.nextInt();
            in.nextInt();

            int entityCount = in.nextInt();
            Unit[] units = new Unit[entityCount];
            for (int i = 0; i < entityCount; i++) {
                int id = in.nextInt();
                int type = in.nextInt();
                int x = in.nextInt();
                int y = in.nextInt();
                int shieldLife = in.nextInt();
                int isControlled = in.nextInt();
                int health = in.nextInt();
                int vx = in.nextInt();
                int vy = in.nextInt();
                int nearBase = in.nextInt();
                int threatFor = in.nextInt();
                units[i] = new Unit(id, type, x, y, shieldLife, isControlled, health, vx, vy, nearBase, threatFor);
            }
            Unit[] myHeroes = Arrays.stream(units).filter(unit -> unit.type == 1).toArray(s -> new Unit[s]);

            int nbHeroesRoaming = 2;

            Unit closestEnemyToBase = null;
            double minDistToBase = Double.POSITIVE_INFINITY;
            for (Unit unit : units) {
                if (unit.type != 0) continue;
                double curDist = computeDist(baseX, baseY, unit.x, unit.y);
                if (curDist < minDistToBase) {
                    minDistToBase = curDist;
                    closestEnemyToBase = unit;
                }
            }

            for (int i = 0; i < nbHeroesRoaming; i++) {
                Unit hero = myHeroes[i];
                
                Unit target = null;
                double minDist = Double.POSITIVE_INFINITY;
                for (Unit unit : units) {
                    if (unit.type != 0 || unit == closestEnemyToBase) continue;
                    double curDist = computeDist(hero, unit);
                    if (curDist < minDist) {
                        minDist = curDist;
                        target = unit;
                    }
                }
                if (target == null) {
                    System.out.println("MOVE " + postX[i] + " " + postY[i]);
                } else {
                    if (canWind(mana) && computeDist(hero.x, hero.y, target.x, target.y) < 1280) {
                        System.out.println("SPELL WIND " + (17630-baseX) + " " + (9000-baseY));
                    } else {
                        System.out.println("MOVE " + target.x + " " + target.y);
                    }
                }
            }

            for (int i = nbHeroesRoaming; i < heroesPerPlayer; i++) {
                Unit hero = myHeroes[i];
                Unit target = closestEnemyToBase;
                
                if (target == null || minDistToBase > 5000) {
                    System.out.println("WAIT");
                } else {
                    if (canWind(mana) && computeDist(hero.x, hero.y, target.x, target.y) < 1280) {
                        System.out.println("SPELL WIND " + postX[i] + " " + postY[i]);
                    } else {
                        System.out.println("MOVE " + target.x + " " + target.y);
                    }
                }
            }
        }
    }
  ```
### \#9 (PR was accepted)
+ Resource Type: org.apache.http.impl.client.CloseableHttpClient;  java.io.BufferedReader 
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#4](https://github.com/Drun1baby/JavaSecurityLearning/pull/4/commits/e9f231313247bb61fe544b8863b6da24ea95b23e)
+ File: JavaSecurity/CodeReview/JavaSec-Code/SSRF/src/main/java/com/drunkbaby/util/HttpUtils.java
  ```java
      public static String httpClient(String url) {

        StringBuilder result = new StringBuilder();

        try {

            CloseableHttpClient client = HttpClients.createDefault();
            HttpGet httpGet = new HttpGet(url);
            // set redirect enable false
            // httpGet.setConfig(RequestConfig.custom().setRedirectsEnabled(false).build());
            HttpResponse httpResponse = client.execute(httpGet); // send request
            BufferedReader rd = new BufferedReader(new InputStreamReader(httpResponse.getEntity().getContent()));

            String line;
            while ((line = rd.readLine()) != null) {
                result.append(line);
            }

            return result.toString();

        } catch (Exception e) {
            return e.getMessage();
        }

  ```

### \#10 (PR was accepted)
+ Resource Type: com.unboundid.ldap.listener.InMemoryDirectoryServer
+ Repository: [JavaSecurityLearning](https://github.com/Drun1baby/JavaSecurityLearning)
+ Pull Request: [pull\#3](https://github.com/Drun1baby/JavaSecurityLearning/pull/3/commits/04d35eea5d683ff3302af9819f66d9fa5f87eb23)
+ File: JavaSecurity/jndi/JndiCode/JndiRMIServer/src/main/java/JNDIGadgetServer.java
  ```java
     public static void main (String[] args) {
        String url = "http://127.0.0.1:7777/#JndiCalc";
        int port = 1234;
        try {
            InMemoryDirectoryServerConfig config = new InMemoryDirectoryServerConfig(LDAP_BASE);
            config.setListenerConfigs(new InMemoryListenerConfig(
                    "listen",
                    InetAddress.getByName("0.0.0.0"),
                    port,
                    ServerSocketFactory.getDefault(),
                    SocketFactory.getDefault(),
                    (SSLSocketFactory) SSLSocketFactory.getDefault()));
            config.addInMemoryOperationInterceptor(new OperationInterceptor(new URL(url)));
            InMemoryDirectoryServer ds = new InMemoryDirectoryServer(config);
            System.out.println("Listening on 0.0.0.0:" + port);
            ds.startListening();
        }
        catch ( Exception e ) {
            e.printStackTrace();
        } finally {
            ds.shutDown(true);
        }
    }
  ```


### \#11
+ Resource Type: java.net.Socket
+ Repository: [doris-manager](https://github.com/apache/doris-manager)
+ Pull Request: [pull\#69](https://github.com/apache/doris-manager/pull/69/commits/90692505ab5775b9fb1c37c299e58d834623b781)
+ File: manager/dm-server/src/main/java/org/apache/doris/stack/util/TelnetUtil.java
  ```java
      public static boolean telnet(String host, int port) {
        Socket socket = new Socket();
        boolean isConnected = false;
        long str = System.currentTimeMillis();
        try {
            socket.connect(new InetSocketAddress(host, port), 1000);
            isConnected = socket.isConnected();
            System.out.println(isConnected);
        } catch (IOException e) {
            log.error("can not telnet {}:{}", host, port);
        } finally {
            try {
            try {
                socket.close();
            } catch (IOException e) {
                log.error("can not telnet {}:{}", host, port);
            }
          }
        System.out.println(System.currentTimeMillis() - str);
        return isConnected;
    }
  ```
### \#12
+ Resource Type: java.io.BufferedReader
+ Repository: [vldbj-trajectory-distance-measures](https://github.com/leoshuncheng/vldbj-trajectory-distance-measures)
+ Pull Request: [pull\#1](https://github.com/leoshuncheng/vldbj-trajectory-distance-measures/pull/1/commits/6d339a4e3c58e0299a0d77d97ee198c2ea7b3cb9)
+ File: /JDBCFactory.java

  ```java
  public static ArrayList<Trajectory> readOriginalTrajectoriesFromGeolife() {
        ArrayList<Trajectory> trajectoryList =
                new ArrayList<Trajectory>();     //Initialize a dynamic array of type Trajectory
        try {
            // open files from folder
            File diretory = new File(INPUT_FILE + ORIGINAL_TRA_FOLDER);

            File files[] = openDirectoryFiles(diretory);
            // read files
            for (int fileId = 0; fileId < files.length; fileId++) {
                File currentFile = files[fileId];
                // read file
                BufferedReader buffer = new BufferedReader(
                        new FileReader(currentFile));
                // fields to be read from the file
                double coordinate[] = new double[DIMENSION];
                // new trajectory for this file, set features
                Trajectory trajectory = new Trajectory();
                // read file lines
                while (buffer.ready()) {
                    String line = buffer.readLine();
                    String[] tokens = line.split(",");
                    // if new trajectory
                    if (tokens.length != 7) {
                        // Add trajectories with more than 20 points only
                        continue;
                    } else {
                        // Parse the inputs
                        String timeString = tokens[5] + " " + tokens[6];
                        coordinate[1] = Double.parseDouble(tokens[0]);
                        coordinate[0] = Double.parseDouble(tokens[1]);
                        SimpleDateFormat format = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                        Date date = null;
                        try {
                            date = format.parse(timeString);
                        } catch (ParseException e) {
                            e.printStackTrace();
                        }
                        // Convert time to timestamp
                        long timeStamp = date.getTime();
                        // create a new point from the line input, set features
                        Point point = new Point(coordinate, timeStamp);
                        trajectory.addPoint(point);
                    }
                }
                // Add trajectories with more than 20 points only
                if (trajectory.numberOfPoints() >= 20 && trajectory.numberOfPoints() <= 150) {
                    trajectoryList.add(trajectory);
                    if (trajectoryList.size() == 5000)
                        break;
                }
                // close file
                buffer.close();
            }
        } catch (IOException e) {
            System.out.println("Error opening input files.");
            e.printStackTrace();
        }
        return trajectoryList;
    }
  ```
  