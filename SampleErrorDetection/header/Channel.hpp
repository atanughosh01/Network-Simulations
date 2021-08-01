#pragma once

#include "Constant.hpp"
#include "Error.hpp"

#include "iostream"
#include "semaphore.h"
#include "fcntl.h"
#include "sys/stat.h"
#include "sys/mman.h"
#include "unistd.h"

using namespace std;

class Channel {
    static const len_t CHAN_SIZE = 2048;
    byte_t* buffer;

    string bufferName;
    string semBufferFullName;
    string semBufferEmptyName;

    sem_t* semBufferFull;
    sem_t* semBufferEmpty;

    indx_t front;
    indx_t rear;
    
    sem_t* initSem(string name, semVal_t val) {
        Error error;
        error.className("Channel");
        error.funcName("initSem");

        sem_t* tmp;
        tmp = sem_open(name.c_str(),O_CREAT|O_EXCL, S_IRUSR|S_IWUSR, val);

        if (tmp == SEM_FAILED) {
            error.problemIs("sem_open failed");
            throw error;
        }

        return tmp;
    }

    byte_t* initBuffer(string name) {
        Error error;
        error.className("Channel");
        error.funcName("initBuffer");

        int fd = shm_open(name.c_str(), O_CREAT|O_RDWR, 0666);

        if(fd == -1) {
            error.problemIs("shm_open failed");
            throw error;
        }

        if (ftruncate(fd, CHAN_SIZE) == -1) {
            error.problemIs("ftruncate failed");
            throw error;
        }

        byte_t* buf = (byte_t *)mmap(NULL, CHAN_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED,fd, 0);

        if(buffer == MAP_FAILED) {
            error.problemIs("mmap failed");
            throw error;
        }

        return buf;
    }

    sem_t* openSem(string name) {
        Error error;
        error.className("Channel");
        error.funcName("openSem");

        sem_t* tmp = sem_open(name.c_str(), 0);
        
        if (tmp == SEM_FAILED) {
            error.problemIs("sem_open failed");
            throw error;
        }

        return tmp;
    }

    byte_t* openBuffer(string name) {
        Error error;
        error.className("Channel");
        error.funcName("openBuffer");

        int fd = shm_open(name.c_str(),O_RDWR, 0);

        if(fd == -1) {
            error.problemIs("shm_open failed");
            throw error;
        }

        if (ftruncate(fd, CHAN_SIZE) == -1) {
            error.problemIs("ftruncate failed");
            throw error;
        }

        byte_t* buf = (byte_t *)mmap(NULL, CHAN_SIZE, PROT_READ|PROT_WRITE, MAP_SHARED,fd, 0);

        if(buffer == MAP_FAILED) {
            error.problemIs("mmap failed");
            throw error;
        }

        return buf;
    }

    void closeBuffer(string name) {
        Error error;
        error.className("Channel");
        error.funcName("closeBuffer");

        if (shm_unlink(name.c_str()) == -1) {
            error.problemIs("shm_unlink failed");
            throw error;
        }

        if(munmap(buffer, CHAN_SIZE) == -1) {
            error.problemIs("munmap failed");
            throw error;
        }
    }

    void closeSem(sem_t* sem, string name) {
        Error error;
        error.className("Channel");
        error.funcName("closeSem");

        if (sem_unlink(name.c_str()) == -1) {
            error.problemIs("sem_unlink failed");
            throw error;
        }

        if(sem_close(sem) == -1) {
            error.problemIs("sem_close failed");
            throw error;
        }
    }


public:
    void init(string bufferName, string semBufferFullName, string semBufferEmptyName) {
        this->bufferName = bufferName;
        this->semBufferEmptyName = semBufferEmptyName;
        this->semBufferFullName = semBufferFullName;

        buffer = initBuffer(bufferName);
        semBufferEmpty = initSem(semBufferEmptyName, 0);
        semBufferFull = initSem(semBufferFullName, CHAN_SIZE);
    }

    void open(string bufferName, string semBufferFullName, string semBufferEmptyName) {
        this->bufferName = bufferName;
        this->semBufferEmptyName = semBufferEmptyName;
        this->semBufferFullName = semBufferFullName;

        buffer = openBuffer(bufferName);
        semBufferEmpty = openSem(semBufferEmptyName);
        semBufferFull = openSem(semBufferFullName);

        front = 0;
        rear = 0;
    }

    void close() {
        closeBuffer(bufferName);
        closeSem(semBufferEmpty, semBufferEmptyName);
        closeSem(semBufferFull, semBufferFullName);
    }

    void write(byte_t data[], len_t len) {
        for (indx_t i = 0; i < len; i++) {
            sem_wait(semBufferFull);
            buffer[front+i] = data[i];
            sem_post(semBufferEmpty);
        }

        front = (front + len)%CHAN_SIZE;
    }

    void read(byte_t data[], len_t len) {
        for (indx_t i = 0; i < len; i++) {
            sem_wait(semBufferEmpty);
            data[i] = buffer[rear+i];
            sem_post(semBufferEmpty);
        }

        rear = (rear + len)%CHAN_SIZE;
    }
};
