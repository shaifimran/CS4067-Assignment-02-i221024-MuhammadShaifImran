FROM eclipse-temurin:17-jdk-alpine

WORKDIR /NotificationService

COPY pom.xml .

RUN apk add --no-cache maven

RUN mvn dependency:go-offline -B

COPY . .

RUN mvn clean package -DskipTests

EXPOSE 5003

CMD ["java", "-jar", "target/notification-service-1.0-SNAPSHOT.jar"]