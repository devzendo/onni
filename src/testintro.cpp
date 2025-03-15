#include "gtest/gtest.h"

class TestIntro : public ::testing::Test {
protected:


    void SetUp() override {
    }

    void TearDown() override {
    }
};

bool doit() {
    return true;
}
TEST_F(TestIntro, GettingStartedExample)
{
    EXPECT_EQ(doit(), true);

}
