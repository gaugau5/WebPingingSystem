import http from "k6/http";
import { check, sleep } from "k6";
import { group } from "k6";
import { Trend } from "k6/metrics";
import { Counter, Rate } from "k6/metrics";
//let response = null;
//let loginTime = new Trend('login_time');
//var loginTime = new Trend("login_time");


let ErrorCount = new Counter("errors");
let ErrorRate = new Rate("error_rate");

export let options = {
    stages: [
        {duration: "30s", target: 60},
        {duration: "30s", target: 100},
        {duration: "20s", target: 0},
        //{iterations: 10}
    ],
    thresholds: {
        error_rate: ["rate<0.5"]
    }
    //thresholds: {
    //    "RTT": ["avg<500"]
    //  }
};

/*var loginTime = new Trend("login_time", true);
var loginTimeDiffTrend = new Trend("login_time_diff", true);
var loginTimeAvg = new Trend("login_time_avg", true);*/

export default function(){
    const path = Math.random() < 0.9 ? "200" : "500";
    let res = http.get("https://httpbin.org/");
    let success = check(res, {
        "status was 200": (r) => r.status == 200
    });

    if(!success){
        ErrorCount.add(1);
        ErrorRate.add(true);
    }else{
        ErrorRate.add(false);
    }

    sleep(1);
};
    /*group("Log In", function(){
        let startTime = Date.now();
        let resp = http.get("https://httpbin.org/");
        let totalTime = Date.now() - startTime;

        loginTime.add(totalTime);
        loginTimeDiffTrend.add(Math.abs(totalTime - resp.timings.duration - resp.timings.blocked));
        loginTimeAvg.add(resp.timings.duration);


        
    })*/
    

  //group("Log In", function(){
  //  let res = http.get("https://httpbin.org/");
  //  let headers = {
  //        headers: {
  //          "accept": "*/*",
  //          "accept-encoding": "gzip, deflate, br",
  //          "connection": "keep-alive"
  //        }
  //  };
    
    
    //response = http.get(res,headers);

    //loginTime.add(response.timings.duration);
    //console.log("The duration for this request was:" + response.timings.duration);

    


    


