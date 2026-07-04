package com.uct.smartfactory.controller;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;
import org.springframework.util.StopWatch;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

@SpringBootTest
@AutoConfigureMockMvc
public class AssetControllerPerformanceTest {

    @Autowired
    private MockMvc mockMvc;

    @Test
    public void testGetAllAssetsPerformanceUnderLoad() throws Exception {
        int concurrentRequests = 100;
        StopWatch stopWatch = new StopWatch();
        
        System.out.println("Starting performance test with " + concurrentRequests + " simulated requests...");
        
        stopWatch.start();
        
        for (int i = 0; i < concurrentRequests; i++) {
            MvcResult result = mockMvc.perform(get("/api/assets"))
                    .andExpect(status().isOk())
                    .andReturn();
        }
        
        stopWatch.stop();
        
        long totalTimeMillis = stopWatch.getTotalTimeMillis();
        double averageTimeMillis = (double) totalTimeMillis / concurrentRequests;
        
        System.out.println("Total Time for " + concurrentRequests + " requests: " + totalTimeMillis + " ms");
        System.out.println("Average Time per request: " + averageTimeMillis + " ms");
        
        // The requirement is that the endpoint responds in under 200ms.
        // We assert that the average response time is under 200ms.
        assertTrue(averageTimeMillis < 200, "Average response time exceeded 200ms!");
    }
}
