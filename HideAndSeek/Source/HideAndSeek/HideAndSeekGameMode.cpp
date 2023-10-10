// Copyright Epic Games, Inc. All Rights Reserved.

#include "HideAndSeekGameMode.h"
#include "HideAndSeekPlayerController.h"
#include "HideAndSeekCharacter.h"
#include "UObject/ConstructorHelpers.h"
#include "OnlineSubsystemUtils.h"
#include "OnlineSubsystem.h"
#include "Interfaces/OnlineIdentityInterface.h"

AHideAndSeekGameMode::AHideAndSeekGameMode()
{
	// use our custom PlayerController class
	PlayerControllerClass = AHideAndSeekPlayerController::StaticClass();

	// set default pawn class to our Blueprinted character
	static ConstructorHelpers::FClassFinder<APawn> PlayerPawnBPClass(TEXT("/Game/TopDown/Blueprints/BP_Red"));
	if (PlayerPawnBPClass.Class != nullptr)
	{
		DefaultPawnClass = PlayerPawnBPClass.Class;
	}

	// set default controller to our Blueprinted controller
	static ConstructorHelpers::FClassFinder<APlayerController> PlayerControllerBPClass(TEXT("/Game/TopDown/Blueprints/BP_TopDownPlayerController"));
	if(PlayerControllerBPClass.Class != NULL)
	{
		PlayerControllerClass = PlayerControllerBPClass.Class;
	}
}

void AHideAndSeekGameMode::PostLogin(APlayerController* NewPlayer)
{
	Super::PostLogin(NewPlayer);
	if (NewPlayer) {
		FUniqueNetIdRepl UniqueNetIDRepl;
		if (NewPlayer->IsLocalController()) {
			ULocalPlayer* LocalPlayerRef = NewPlayer->GetLocalPlayer();
			if (LocalPlayerRef) {
				UniqueNetIDRepl = LocalPlayerRef->GetPreferredUniqueNetId();
			}
			else {
				UNetConnection* RemoteNetConnectionRef = Cast<UNetConnection>(NewPlayer->Player);
				check(IsValid(RemoteNetConnectionRef));
				UniqueNetIDRepl = RemoteNetConnectionRef->PlayerId;
			}
		}
		else {
			UNetConnection* RemoteNetConnectionRef = Cast<UNetConnection>(NewPlayer->Player);
			check(IsValid(RemoteNetConnectionRef));
			UniqueNetIDRepl = RemoteNetConnectionRef->PlayerId;
		}

		TSharedPtr<const FUniqueNetId> UniqueNetId = UniqueNetIDRepl.GetUniqueNetId();
		if (UniqueNetId != nullptr) {
			IOnlineSubsystem* SubsystemRef = Online::GetSubsystem(NewPlayer->GetWorld());
			IOnlineSessionPtr SessionRef = SubsystemRef->GetSessionInterface();
			bool bRegistrationSuccess = SessionRef->RegisterPlayer(FName("MainSession"), *UniqueNetId, false);
			if (bRegistrationSuccess) {
				UE_LOG(LogTemp, Warning, TEXT("Registration Successful"));
			}
		}
	}
}
