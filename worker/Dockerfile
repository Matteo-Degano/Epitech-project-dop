FROM maven:3.8.4-jdk-11-slim AS builder

WORKDIR /app

COPY pom.xml .

RUN mvn dependency:resolve

COPY . .

RUN mvn -f /app/pom.xml package

FROM openjdk:11-jre-slim

COPY --from=builder /app/target/worker-jar-with-dependencies.jar .

CMD ["java","-jar","worker-jar-with-dependencies.jar"]