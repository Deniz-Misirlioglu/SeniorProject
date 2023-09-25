// Fill out your copyright notice in the Description page of Project Settings.


#include "EOS_GameInstance.h"
#include "OnlineSubsystemUtils.h"
#include "OnlineSubsystem.h"
#include "Interfaces/OnlineIdentityInterface.h"

void UEOS_GameInstance::LoginWithEOS(FString ID, FString Token, FString LoginType)
{
	IOnlineSubsystem* SubsystemRef = Online::GetSubsystem(this->GetWorld());
	if (SubsystemRef) {

		IOnlineIdentityPtr IdentityPointerRef = SubsystemRef->GetIdentityInterface();
		if (IdentityPointerRef) {
			FOnlineAccountCredentials AccountDetails;
			AccountDetails.Id = ID;
			AccountDetails.Token = Token;
			AccountDetails.Type = LoginType;
			IdentityPointerRef->OnLoginCompleteDelegates->AddUObject(this,&UEOS_GameInstance::LoginWithEOS_Return);
			IdentityPointerRef->Login(0,AccountDetails);
		}
	}
}

FString UEOS_GameInstance::GetPlayerUsername()
{
	IOnlineSubsystem* SubsystemRef = Online::GetSubsystem(this->GetWorld());
	if (SubsystemRef) {

		IOnlineIdentityPtr IdentityPointerRef = SubsystemRef->GetIdentityInterface();
		if (IdentityPointerRef) {
			if (IdentityPointerRef->GetLoginStatus(0) == ELoginStatus::LoggedIn) {
				return IdentityPointerRef->GetPlayerNickname(0);
			}
		}
	}
	return FString();
}

bool UEOS_GameInstance::IsPlayerLoggedIn()
{
	IOnlineSubsystem* SubsystemRef = Online::GetSubsystem(this->GetWorld());
	if (SubsystemRef) {

		IOnlineIdentityPtr IdentityPointerRef = SubsystemRef->GetIdentityInterface();
		if (IdentityPointerRef) {
			if (IdentityPointerRef->GetLoginStatus(0) == ELoginStatus::LoggedIn) {
				return true;
			}
		}
	}
	return false;
}

void UEOS_GameInstance::LoginWithEOS_Return(int32 LocalUserNum, bool bWasSuccess, const FUniqueNetId& UserId, const FString& Error)
{
	if (bWasSuccess) {
		UE_LOG(LogTemp, Warning, TEXT("Login Success"));
	}
	else {
		UE_LOG(LogTemp, Error, TEXT("Login Fail Reason - %S"), *Error);
	}
}

void UEOS_GameInstance::OnCreateSessionCompleted(FName SessionName, bool bWasSuccessful)
{
	if (bWasSuccessful) {
		GetWorld()->ServerTravel(OpenLevelText);
	}
}

void UEOS_GameInstance::CreateEOSSession(bool bIsDedicatedServer, bool bIsLanServer, int32 NumberOfPublicConnections)
{
	IOnlineSubsystem* SubsystemRef = Online::GetSubsystem(this->GetWorld());
	if (SubsystemRef) {
		IOnlineSessionPtr SessionPtrRef = SubsystemRef->GetSessionInterface();
		if (SessionPtrRef) {
			FOnlineSessionSettings SessionCreationInfo;
			SessionCreationInfo.bIsDedicated = bIsDedicatedServer;
			SessionCreationInfo.bAllowInvites = true;
			SessionCreationInfo.bIsLANMatch = bIsLanServer;
			SessionCreationInfo.NumPublicConnections = NumberOfPublicConnections;
			SessionCreationInfo.bUseLobbiesIfAvailable = true; // change if we want lobby
			SessionCreationInfo.bUsesPresence = false;
			SessionCreationInfo.bShouldAdvertise = true;
			SessionCreationInfo.Set(SEARCH_KEYWORDS, FString("RandomHi"), EOnlineDataAdvertisementType::ViaOnlineService);
			SessionPtrRef->OnCreateSessionCompleteDelegates.AddUObject(this, &UEOS_GameInstance::OnCreateSessionCompleted);
			SessionPtrRef->CreateSession(0,FName("MainSession"), SessionCreationInfo);
		}
	}
}

void UEOS_GameInstance::FindSessionAndJoin()
{
}

void UEOS_GameInstance::JoinSession()
{
}
