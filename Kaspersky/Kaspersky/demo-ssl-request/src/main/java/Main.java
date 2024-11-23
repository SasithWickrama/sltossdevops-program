import org.apache.http.conn.ssl.NoopHostnameVerifier;

import javax.net.ssl.*;
import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.security.*;
import java.security.cert.CertificateException;

public class Main {
    public static void main(String[] args) {
        try {
            KeyStore clientStore = KeyStore.getInstance("PKCS12");
            clientStore.load(new FileInputStream(new File("/home/yehancha/Downloads/Kaspersky/kspy.pfx")), "89)iopJKL".toCharArray());
            KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
            kmf.init(clientStore, "89)iopJKL".toCharArray());
            KeyManager[] kms = kmf.getKeyManagers();

            System.out.println("One");

            // Assuming that you imported the CA Cert "Subject: CN=MBIIS CA, OU=MBIIS, O=DAIMLER, C=DE"
            // to your cacerts Store.
            KeyStore trustStore = KeyStore.getInstance("JKS");
            trustStore.load(new FileInputStream("/usr/lib/jvm/default-java/lib/security/cacerts"), "changeit".toCharArray());

            System.out.println("Two");

            TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
            tmf.init(trustStore);
            TrustManager[] tms = tmf.getTrustManagers();

            System.out.println("Three");

            final SSLContext sslContext = SSLContext.getInstance("SSL");
            sslContext.init(kms,tms,new SecureRandom());
            SSLContext.setDefault(sslContext);

            System.out.println("Four");

            HostnameVerifier hostnameVerifier = NoopHostnameVerifier.INSTANCE;
            System.setProperty("https.proxyHost", "https://api.demo.korm.kaspersky.com");
            System.setProperty("https.proxyPort", "443");
            System.setProperty("http.proxySet", "true");
            HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());
            HttpsURLConnection.setDefaultHostnameVerifier(hostnameVerifier);

            System.out.println("Five");

            URL url = new URL("https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/create");

            HttpsURLConnection con =    (HttpsURLConnection)url.openConnection();
            con.setRequestMethod("POST");
            con.setRequestProperty("Content-Type", "application/json; utf-8");
            con.setRequestProperty("Accept", "application/json");
            con.setRequestProperty("User-Agent", "PostmanRuntime/7.26.10");
            con.setRequestProperty("Accept", "*/*");
            con.setRequestProperty("Accept-Encoding", "gzip, deflate, br");
            con.setRequestProperty("Connection", "keep-alive");
//            con.setConnectTimeout(1000);
            con.setSSLSocketFactory(sslContext.getSocketFactory());

            System.out.println("Six");

//            con.connect();
//            BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream()));
//            StringBuilder sb = new StringBuilder();
//            String line;
//            while ((line = br.readLine()) != null) {
//                sb.append(line+"\n");
//            }
//            br.close();
//            System.out.println(sb.toString());

            printResponse(con);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void demoGet() throws IOException {
        HttpsURLConnection con = getCon("GET", "https://www.google.com");
        printResponse(con);
    }

    private static void demoPost() throws IOException, UnrecoverableKeyException, CertificateException, NoSuchAlgorithmException, KeyStoreException, KeyManagementException {
        String body = "{ \\r\\n   \\\"BillingPlan\\\":\\\"Yearly\\\",\\r\\n   \\\"Sku\\\":\\\"KL3111JAKFG\\\",\\r\\n   \\\"Quantity\\\":10,\\r\\n   \\\"Expiration\\\":null,\\r\\n   \\\"Customer\\\":{ \\r\\n      \\\"Contacts\\\":{ \\r\\n         \\\"CompanyName\\\":\\\"Paramount\\\",\\r\\n         \\\"Email\\\":\\\"test.ya.ru\\\",\\r\\n         \\\"Phone\\\":\\\"123456\\\",\\r\\n         \\\"CustomerCode\\\":\\\"1122\\\"\\r\\n      },\\r\\n      \\\"Address\\\":{ \\r\\n         \\\"AddressLine1\\\":\\\"10300 Broadway st.\\\",\\r\\n         \\\"AddressLine2\\\":\\\"smh\\\",\\r\\n         \\\"City\\\":\\\"New York\\\",\\r\\n         \\\"State\\\":\\\"New York\\\",\\r\\n         \\\"Zip\\\":\\\"10025\\\",\\r\\n         \\\"Country\\\":\\\"USA\\\"\\r\\n      }\\r\\n   },\\r\\n   \\\"Distributor\\\":{ \\r\\n      \\\"Partner\\\":\\\"SLT\\\",\\r\\n      \\\"Reseller\\\":\\\"TE27PT00\\\"\\r\\n   },\\r\\n   \\\"Comment\\\":\\\"It's just test!\\\",\\r\\n   \\\"DeliveryEmail\\\":\\\"your@email.com\\\"\\r\\n}";

        HttpsURLConnection con = getCon("POST", "https://api.demo.korm.kaspersky.com/Subscriptions/v2.0/api/Subscription/create");
        setKeyFile(con);
        setRequestBody(con, body);
        printResponse(con);
    }

    private static HttpsURLConnection getCon(String method, String urlString) throws IOException {
        URL url = new URL (urlString);
        HttpsURLConnection con = (HttpsURLConnection)url.openConnection();
        con.setRequestMethod(method);
        con.setRequestProperty("Content-Type", "application/json; utf-8");
        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty("User-Agent", "PostmanRuntime/7.26.10");
        con.setRequestProperty("Accept", "*/*");
        con.setRequestProperty("Accept-Encoding", "gzip, deflate, br");
        con.setRequestProperty("Connection", "keep-alive");
        con.setDoOutput(true);

        return con;
    }

    private static void setKeyFile(HttpsURLConnection con) throws KeyStoreException, IOException, CertificateException, NoSuchAlgorithmException, UnrecoverableKeyException, KeyManagementException {
        KeyStore ks = KeyStore.getInstance("PKCS12");
        FileInputStream fis = new FileInputStream("/home/yehancha/Downloads/Kaspersky/kspy.pfx");
        ks.load(fis, "89)iopJKL".toCharArray());
        KeyManagerFactory kmf = KeyManagerFactory.getInstance(KeyManagerFactory.getDefaultAlgorithm());
        kmf.init(ks, "89)iopJKL".toCharArray());
        SSLContext sc = SSLContext.getInstance("TLSv1.2");
        KeyManager[] kms = kmf.getKeyManagers();
        sc.init(kms, null, null);

        KeyStore trustStore = KeyStore.getInstance("JKS");
        trustStore.load(new FileInputStream("/home/yehancha/Downloads/Kaspersky/kspy.pfx"), "89)iopJKL".toCharArray());

        TrustManagerFactory tmf = TrustManagerFactory.getInstance(TrustManagerFactory.getDefaultAlgorithm());
        tmf.init(trustStore);
        TrustManager[] tms = tmf.getTrustManagers();

        final SSLContext sslContext = SSLContext.getInstance("TLS");
        sslContext.init(kms,tms,new SecureRandom());
        SSLContext.setDefault(sslContext);

        con.setSSLSocketFactory(sc.getSocketFactory());

        System.setProperty("https.proxyHost", "api.demo.korm.kaspersky.com");
        System.setProperty("https.proxyPort", "443");
        HttpsURLConnection.setDefaultSSLSocketFactory(sslContext.getSocketFactory());

        con.setConnectTimeout(10000);
        con.setSSLSocketFactory(sslContext.getSocketFactory());
        con.connect();
    }

    private static void setRequestBody(HttpURLConnection con, String body) throws IOException {
        try (OutputStream os = con.getOutputStream()) {
            byte[] input = body.getBytes("utf-8");
            os.write(input, 0, input.length);
        }
    }

    private static void printResponse(HttpURLConnection con) throws IOException {
        int code = con.getResponseCode();
        System.out.println("Response code: " + code);

        if (code == 200 || code == 201) {
            try (BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "utf-8"))) {
                StringBuilder response = new StringBuilder();
                String responseLine = null;
                while ((responseLine = br.readLine()) != null) {
                    response.append(responseLine.trim());
                }
                System.out.println(response.toString());
            }
        }
    }
}
