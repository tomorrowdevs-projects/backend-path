# Dockerizing an Authentication Service

**Objective:** Containerize an authentication service.

**Real-world Scenario:** You have an application that requires an authentication service. By containerizing this service, you can easily manage authentication in a distributed environment.

**Example Code:**
```java
// AuthenticationController.java
@RestController
@RequestMapping("/auth")
public class AuthenticationController {

    @PostMapping("/login")
    public ResponseEntity<String> login(@RequestBody UserCredentials credentials) {
        // Authentication handling code
        return ResponseEntity.ok("Login successful!");
    }
}
