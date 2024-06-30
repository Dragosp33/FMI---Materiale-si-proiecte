package sql;
import java.sql.*; 

public class MysqlCon{  
    private String driver, site, user, parola, database;
    private int port;
    Connection conn;

    public Connection getConnection(){ return this.conn;}

    public MysqlCon(String driver, String site, String user, String parola, String database, int port) {
        this.driver = driver; this.site = site; this.user = user; this.parola = parola; this.database = database;
        this.port = port;
        
    }

    public MysqlCon() {
        this.driver = "mysql"; this.site = "localhost"; this.user = "root"; this.parola = "root";
        this.database = "proiect_pao";
        this.port = 3308;
    }

    public void connection() {  
    try{  
        Class.forName("com.mysql.cj.jdbc.Driver");  
        this.conn =DriverManager.getConnection(  
        "jdbc:mysql://localhost:3308/proiect_pao","root","root");  
 

        
    }catch(Exception e){ System.out.println(e);}  
    
    }

    public void close_con(){  // inchidere conexiune la iesirea din program
        try {
            this.conn.close();
        } catch (SQLException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }


    public void insert_bank(String Name) {
        this.connection();
        if (this.conn != null){
           try{ PreparedStatement stmt=this.conn.prepareStatement("insert into banks(bank_name) values(?)");
            stmt.setString(1, Name);
            int i=stmt.executeUpdate();  
            System.out.println(i+" records inserted"); 
        }catch(Exception e){ System.out.println(e);}
    
        }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}

    }


    public ResultSet selectAllBanks() {
        this.connection();
        if (this.conn != null){
            


            try{ PreparedStatement stmt=this.conn.prepareStatement("select bank_name from banks");  
             ResultSet rs=stmt.executeQuery(); 
             return rs;
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
        return null;
    }


    public ResultSet selectAllAccounts(){
        this.connection();
        if (this.conn != null){
            


            try{ PreparedStatement stmt=this.conn.prepareStatement("select * from accounts");  
             ResultSet rs=stmt.executeQuery(); 
             return rs;
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
        return null;
    }
    

    public ResultSet selectAllCustomers() {
        this.connection();
        if (this.conn != null){
            


            try{ PreparedStatement stmt=this.conn.prepareStatement("select * from customers");  
             ResultSet rs=stmt.executeQuery(); 
             return rs;
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
        return null;

    }

// join pe tabelel customers, accounts, banks
// pentru a gasi usor conturile si clientii fiecarei banci;

    public ResultSet join_Customers_Accounts_Banks(String banca) {
        this.connection();
        if (this.conn != null){
            


            try{
                String sql2 = "SELECT * FROM accounts, customers where accounts.banca_nume = ? and accounts.acc_number = customers.acc";
                PreparedStatement stmt=this.conn.prepareStatement(sql2);
                stmt.setString(1, banca);
             ResultSet rs=stmt.executeQuery(); 
             return rs;
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
        return null;

    }

//functie update balance, folosita atat pentru retrageri cat si pentru depuneri;

    public void update_balance(int acc_no, double balance) {
        this.connection();
        if (this.conn != null){
            


            try{
                PreparedStatement stmt=this.conn.prepareStatement("update accounts set balance=? where acc_number=?");  
                
                stmt.setDouble(1, balance); 
                stmt.setInt(2,acc_no);
                int i=stmt.executeUpdate(); 
                System.out.println(i+" records updated");
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
    }

//Functie adaugare cont bancar;

    public void insert_account(Double balance, String acctype, String bank_Name){
        this.connection();
        if (this.conn != null){

           try{
            Double roi = 0.02;  
            if (balance > 10000) { roi = 0.05;}
            String sql2 = "insert into accounts(balance, interest, acc_type, banca_nume) values(?,?,?,?)";
            PreparedStatement stmt=this.conn.prepareStatement(sql2);
            
            stmt.setDouble(1, balance);
            stmt.setDouble(2, roi);
            stmt.setString(3, acctype);
            stmt.setString(4, bank_Name);


            int i=stmt.executeUpdate();  
            System.out.println(i+" records inserted"); 
        }catch(Exception e){ System.out.println(e);}
    
        }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}

    }


//Functie adaugare client

    public void insert_customer(String ssid, String firstname, String lastname, int acc){
        this.connection();
        if (this.conn != null){

           try{
            
            String sql2 = "insert into customers(ssid, c_first_name, c_last_name, acc) values(?,?,?,?)";
            PreparedStatement stmt=this.conn.prepareStatement(sql2);
            
            stmt.setString(1, ssid);
            stmt.setString(2, firstname);
            stmt.setString(3, lastname);
            stmt.setInt(4, acc);


            int i=stmt.executeUpdate();  
            System.out.println(i+" records inserted"); 
        }catch(Exception e){ System.out.println(e);}
    
        }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}

    }


    public int getMaxRecords() { 
        this.connection();
        if (this.conn != null){
            


            try{ PreparedStatement stmt=this.conn.prepareStatement("select max(acc_number) from accounts");  
             ResultSet rs=stmt.executeQuery(); 
             rs.next();
             return rs.getInt(1);
         }catch(Exception e){ System.out.println(e);}
     
         }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
        return 0;

    }

    public void delete_account(int accno){
        this.connection();
        if (this.conn != null){
            


            try{
                PreparedStatement stmt=this.conn.prepareStatement("DELETE FROM accounts WHERE acc_number=?");  
                
                stmt.setInt(1, accno); 
                int i=stmt.executeUpdate(); 
            }catch(Exception e){ System.out.println(e);}
        }else{System.out.println("Nu s-a putut efectua conectarea la baza de date");}
    }

 /*   public ResultSet Update_Account() {

    }
*/
}